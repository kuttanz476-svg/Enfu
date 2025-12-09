#!/usr/bin/env python3
"""
server.py — Secure Content Analysis API (Flask) — final combined version
Adjusted so Gunicorn can import `app` directly (module-level app variable).
"""
from __future__ import annotations
import os
import re
import json
import logging
import hmac
from typing import List, Dict, Any
from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Initialize logging early so warnings are emitted via logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
if not API_KEY:
    logging.warning("API_KEY not set. Server routes will reject requests without a valid key.")

# Size guard constants
MAX_TEXT_LENGTH = 100_000
MAX_MESSAGE_LENGTH = 20_000
MAX_MESSAGES = 2000

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of text using keyword matching.
    Returns a dict: {'sentiment': str, 'score': float, 'confidence': float}
    """
    positive_words = {
        'good','great','excellent','amazing','wonderful','fantastic',
        'love','best','awesome','perfect','brilliant','outstanding',
        'superb','happy','joy','beautiful','like','enjoy','positive'
    }
    negative_words = {
        'bad','terrible','awful','horrible','worst','hate','dislike',
        'poor','disappointing','sad','angry','annoying','frustrating',
        'useless','broken','fail','problem','issue','negative','ugly'
    }
    words = re.findall(r'\b\w+\b', (text or "").lower())
    if not words:
        return {'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.0}

    pos = sum(1 for w in words if w in positive_words)
    neg = sum(1 for w in words if w in negative_words)
    total = pos + neg
    if total == 0:
        return {'sentiment': 'neutral', 'score': 0.0, 'confidence': 0.5}

    # score normalized by number of sentiment words
    score = (pos - neg) / total
    confidence = total / len(words)
    sentiment = 'positive' if score > 0.1 else 'negative' if score < -0.1 else 'neutral'
    return {'sentiment': sentiment, 'score': round(score, 3), 'confidence': round(confidence, 3)}

def classify_viewer(text: str, messages: List[str]) -> Dict[str, Any]:
    """
    Classify viewer engagement type based on message patterns.
    Returns dict with viewer_type, engagement_level, characteristics, and metrics.
    """
    messages = list(messages or [])
    if messages:
        word_count = sum(len(re.findall(r'\b\w+\b', m)) for m in messages)
        question_count = sum(m.count('?') for m in messages)
    else:
        word_count = len(re.findall(r'\b\w+\b', text or ""))
        question_count = text.count('?')

    message_count = len(messages)
    avg_length = word_count / max(message_count, 1)
    engagement_words = {'how','why','what','when','where','explain','tell','show','help','please','thanks','thank','appreciate','interested'}
    engagement_score = sum(
        sum(1 for w in re.findall(r'\b\w+\b', m.lower()) if w in engagement_words)
        for m in messages
    )

    if message_count > 5 and avg_length > 10:
        vt = 'power_user'; el = 'high'; ch = ['frequent_interactor', 'detailed_messages', 'highly_engaged']
    elif question_count > 2 or engagement_score > 3:
        vt = 'curious_learner'; el = 'medium-high'; ch = ['asks_questions', 'seeks_information', 'engaged']
    elif word_count > 50:
        vt = 'active_participant'; el = 'medium'; ch = ['provides_input', 'moderate_engagement']
    elif message_count > 0:
        vt = 'casual_viewer'; el = 'low-medium'; ch = ['occasional_interaction', 'brief_messages']
    else:
        vt = 'passive_observer'; el = 'low'; ch = ['minimal_interaction', 'lurker']

    return {
        'viewer_type': vt,
        'engagement_level': el,
        'characteristics': ch,
        'metrics': {
            'message_count': message_count,
            'avg_message_length': round(avg_length, 1),
            'question_count': question_count,
            'engagement_score': engagement_score
        }
    }

class ContentAnalyzer:
    """
    Combined content analyzer that performs sentiment analysis and viewer classification.
    """
    def analyze(self, text: str, messages: List[str] = None) -> Dict[str, Any]:
        messages = messages or []
        s = analyze_sentiment(text)
        v = classify_viewer(text, messages)
        return {
            'sentiment': s,
            'viewer_classification': v,
            'analysis_summary': {
                'total_words': len(re.findall(r'\b\w+\b', text or "")),
                'total_messages': len(messages),
                'overall_tone': s['sentiment'],
                'user_profile': v['viewer_type']
            }
        }

def create_app() -> Flask:
    """
    Factory function to create and configure Flask application.
    """
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB
    limiter = Limiter(app, key_func=get_remote_address, default_limits=["60 per minute"])
    analyzer = ContentAnalyzer()

    def check_key():
        key = request.headers.get("X-API-KEY", "")
        # Use constant-time comparison to mitigate timing attacks
        if not API_KEY or not hmac.compare_digest(str(key), str(API_KEY)):
            abort(401, description="invalid or missing API key")

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({'error': 'payload_too_large'}), 413

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({'status': 'ok'})

    @app.route("/analyze", methods=["POST"])
    @limiter.limit("30 per minute")
    def analyze_route():
        check_key()
        if not request.is_json:
            return jsonify({'error': 'expected_application_json'}), 400
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        messages = data.get("messages", [])

        # Validate input types
        if not isinstance(text, str):
            return jsonify({'error': 'text_must_be_string'}), 400
        if not isinstance(messages, list):
            return jsonify({'error': 'messages_must_be_list'}), 400

        # Validate message contents
        if not all(isinstance(m, str) for m in messages):
            return jsonify({'error': 'invalid_messages'}), 400

        # Enforce size limits
        if len(text) > MAX_TEXT_LENGTH:
            return jsonify({'error': 'text_too_large', 'max': MAX_TEXT_LENGTH}), 413
        if len(messages) > MAX_MESSAGES:
            return jsonify({'error': 'too_many_messages', 'max': MAX_MESSAGES}), 413
        for idx, m in enumerate(messages):
            if len(m) > MAX_MESSAGE_LENGTH:
                return jsonify({'error': 'message_too_large', 'index': idx, 'max': MAX_MESSAGE_LENGTH}), 413

        # Minimal logging (do not log raw text/messages)
        logging.info(
            "analyze called: path=%s ip=%s words=%d messages=%d",
            request.path, request.remote_addr, len(re.findall(r'\b\w+\b', text or "")), len(messages)
        )

        # Perform analysis with error capture
        try:
            result = analyzer.analyze(text, messages)
            return jsonify(result), 200
        except Exception:
            logging.exception("Analysis failed")
            return jsonify({'error': 'analysis_failed'}), 500

    return app

# Create a module-level app so Gunicorn can import `server:app` directly.
# This avoids using --factory and prevents start-command mismatch issues.
app = create_app()

def run_demo():
    """CLI demo that doesn't require an API key."""
    analyzer = ContentAnalyzer()
    samples = [
        {'text': 'This is amazing! I love it.', 'messages': ['This is amazing!', 'I love it.']},
        {'text': 'Terrible experience, I hate it', 'messages': ['Terrible experience', 'I hate it']}
    ]

    # Pretty-print demo results for readability
    for i, s in enumerate(samples, 1):
        print(f"\nSample {i}:")
        print(json.dumps(analyzer.analyze(s['text'], s['messages']), indent=2))

if __name__ == "__main__":
    import sys
    # Allow local run for development:
    if len(sys.argv) > 1 and sys.argv[1] == "--run-demo":
        run_demo()
    else:
        host = os.getenv("HOST", "127.0.0.1")
        port = int(os.getenv("PORT", "3000"))
        print(f"Server starting on http://{host}:{port}")
        # Only start the built-in dev server when running directly (not under Gunicorn)
        app.run(host=host, port=port, debug=False)
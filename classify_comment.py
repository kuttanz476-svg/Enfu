"""
classify_comment.py

Usage:
  - Set environment variable HUGGINGFACE_TOKEN if you want to use Hugging Face inference.
  - Run: python classify_comment.py "the comment text here"

Behavior:
  - If HUGGINGFACE_TOKEN is set, the script reads classification_prompt.md,
    inserts the comment, calls the HF inference API (model variable below),
    and prints the single-line classification returned by the model.
  - If no token is provided, a simple deterministic fallback rule-based
    classifier runs locally (guaranteed deterministic, useful for testing).
"""

import os
import sys
import json
import requests
import re

# Change to an available instruct model on Hugging Face if needed
HF_MODEL = "mistralai/Mistral-7B-Instruct"  # replace if you prefer another hosted model

PROMPT_FILE = "classification_prompt.md"

def load_prompt():
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(template, comment):
    return template.replace("{{comment}}", comment.strip())

def call_hf_inference(prompt, model=HF_MODEL, token=None, timeout=30):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 64, "temperature": 0.0}}
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    # Different HF backends return different shapes. Handle common cases:
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError("HF error: " + data["error"])
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"].strip()
    # Some endpoints return a simple string inside the first element
    if isinstance(data, list) and isinstance(data[0], dict) and "text" in data[0]:
        return data[0]["text"].strip()
    # Fallback: try to stringify
    return str(data).strip()

def fallback_classifier(comment):
    c = comment.lower()
    # simple deterministic rules — modify rules as you iterate
    if any(w in c for w in ["love", "so good", "amazing", "😍", "❤️", "best"]):
        return "Emotional Viewer"
    if any(w in c for w in ["buy", "where can i", "link", "coupon", "price", "order"]):
        return "Impulsive Viewer"
    if any(w in c for w in ["always", "followed", "since day 1", "loyal", "been here"]):
        return "Loyal Viewer"
    if len(c.split()) <= 2:
        return "Passive Viewer"
    if any(w in c for w in ["trend", "viral", "challenge", "tiktok", "meme"]):
        return "Trend-Triggered Viewer"
    if any(w in c for w in ["fake", "scam", "worst", "terrible", "hate", "critic"]):
        return "Critical Viewer"
    return "Passive Viewer"

def sanitize_model_output(text):
    # keep only the expected labels if present
    labels = [
        "Emotional Viewer",
        "Impulsive Viewer",
        "Loyal Viewer",
        "Passive Viewer",
        "Trend-Triggered Viewer",
        "Critical Viewer"
    ]
    # try exact match first
    for lbl in labels:
        if re.search(r"\b" + re.escape(lbl) + r"\b", text, flags=re.IGNORECASE):
            return lbl
    # fallback: return the clean first line
    return text.splitlines()[0].strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python classify_comment.py \"comment text here\"")
        sys.exit(1)

    comment = sys.argv[1].strip()
    prompt_template = load_prompt()
    prompt = build_prompt(prompt_template, comment)
    hf_token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN") or None

    if hf_token:
        try:
            raw = call_hf_inference(prompt, token=hf_token)
            out = sanitize_model_output(raw)
            print(out)
            return
        except Exception as e:
            print("Warning: HF call failed, falling back to local rules. Error:", e, file=sys.stderr)

    # Fallback deterministic classifier
    out = fallback_classifier(comment)
    print(out)

if __name__ == "__main__":
    main()
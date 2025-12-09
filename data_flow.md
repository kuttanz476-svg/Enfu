# ENFU Data Flow

1. **Scraper → raw_data/**
   - Scraper outputs JSON files.
   - Example: raw_data/influencer123_2025-01-01.json

2. **raw_data → clean_data/**
   - Run cleaning script.
   - Remove emojis, links, duplicates.
   - Save as clean_data/influencer123_clean.json

3. **clean_data → Viewer Type Classifier**
   - For each comment:
     - Run classification_prompt.md
     - Save as viewer_type field.

4. **clean_data → Sentiment Analyzer**
   - For each comment:
     - Run sentiment_prompt.md
     - Save as sentiment field.

5. **Viewer Types + Sentiment → audience_profile.json**
   - Count viewer types.
   - Count sentiment categories.
   - Extract trending keywords.

6. **audience_profile.json → Sponsorship Score**
   - Apply formula from sponsorship_score.md
   - Output a score (0–100).

7. **audience_profile + performance → Content Strategy**
   - Run content_prompt.md
   - Output one idea + reason.

8. **DM inbox → DM Classifier**
   - Run dm_classifier_prompt.md
   - Output sorted categories.

9. **Final Output → outputs/**
   - Save:
     - sponsorship_score.json
     - audience_profile.json
     - content_idea.json
     - dm_sorted.json
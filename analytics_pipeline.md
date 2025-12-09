# ENFU Analytics Pipeline (Step-by-Step)

1. **Collect Data**
   - Scrape public comments, captions, and basic metrics.
   - Store raw data in /raw_data/.

2. **Clean Data**
   - Remove emojis, links, repeated characters.
   - Normalize text.
   - Save cleaned data in /clean_data/.

3. **Classify Viewer Types**
   - For each comment, run classification_prompt.md.
   - Store the result as viewer_type.

4. **Analyze Sentiment**
   - For each comment, run sentiment_prompt.md.
   - Store sentiment value.

5. **Aggregate Audience Profile**
   - Count each viewer type.
   - Count sentiment distribution.
   - Extract trending topics (top keywords).
   - Save result as audience_profile.json.

6. **Compute Sponsorship Score**
   - Use sponsorship_score.md formula.
   - Output single number (0–100).

7. **Generate Content Strategy**
   - Input audience_profile.json + recent performance.
   - Run content_prompt.md.
   - Output one content idea and reason.

8. **Classify DMs**
   - For each DM, run dm_classifier_prompt.md.
   - Sort into 5 categories.
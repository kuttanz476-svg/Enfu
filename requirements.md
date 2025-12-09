# ENFU Requirements (Minimal)

## Accounts Needed
- GitHub (project code + version control)
- Apify Free Tier (scraping)
- HuggingFace (open models)
- Claude.ai (reasoning + strategy generation)

## Python Libraries
- pandas (data handling)
- numpy (math operations)
- nltk (text cleaning)
- scikit-learn (keyword extraction)
- requests (API calls)
- beautifulsoup4 (fallback scraping)
- json (file handling)

## Folder Structure
- raw_data/
- clean_data/
- models/
- services/
- prompts/
- outputs/

## File Dependencies
- schema.json
- viewer_types.json
- classification_prompt.md
- sentiment_prompt.md
- content_prompt.md
- dm_classifier_prompt.md
- sponsorship_score.md
- analytics_pipeline.md

## Hardware Requirements
- Any laptop or cloud VM with Python installed
- No GPU required for MVP (we use hosted models)
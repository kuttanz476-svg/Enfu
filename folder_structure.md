# ENFU Project Folder Structure

/root
  ├── raw_data/            # Unprocessed scraped data
  ├── clean_data/          # Cleaned comments and messages
  ├── models/              # Local or hosted model configs
  ├── services/            # API logic, pipelines
  ├── prompts/             # All AI prompt files
  ├── outputs/             # Final analytics results

# Required Files in prompts/
  - classification_prompt.md
  - sentiment_prompt.md
  - content_prompt.md
  - dm_classifier_prompt.md

# Required Files in root/
  - schema.json
  - viewer_types.json
  - sponsorship_score.md
  - analytics_pipeline.md
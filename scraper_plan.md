# ENFU Scraper Plan (Free Tools)

ENFU will use free or freemium services to collect influencer data.

## 1. Tools
- **Apify Free Tier**  
  - Instagram Scraper  
  - TikTok Scraper  
  - YouTube Comments Scraper  
- Output saved as JSON or CSV.

## 2. Data Collected
- Post captions  
- Post comments  
- Like count  
- Comment count  
- Timestamp  
- Basic profile info (followers, profile link)

## 3. Storage
- Save original data inside /raw_data/ folder.
- Filename format: influencer_username_timestamp.json

## 4. Cleaning Step
- Remove emojis  
- Remove URLs  
- Normalize text  
- Remove duplicates  
- Save cleaned file into /clean_data/

## 5. Limits
- Avoid login-based scrapers.  
- Keep requests low to avoid rate limits.  
- Free tier is enough for MVP.

## 6. Next Action
After scraping → run analytics_pipeline.md steps.
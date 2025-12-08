# ENFU ANALYTICS — DATA MODEL (DRAFT)

## USERS
- id (uuid)
- email
- password_hash (or external auth id)
- created_at
- updated_at

## SOCIAL_ACCOUNTS
- id (uuid)
- user_id (fk → USERS.id)
- platform (e.g. "instagram", "twitter")
- handle
- external_account_id
- access_token (encrypted or stored in provider)
- refresh_token (optional)
- connected_at
- last_synced_at

## POSTS
- id (uuid)
- social_account_id (fk → SOCIAL_ACCOUNTS.id)
- external_post_id
- posted_at
- content_type (image / video / reel / text)
- caption_preview (first 140 chars)
- url

## POST_STATS
- id (uuid)
- post_id (fk → POSTS.id)
- captured_at
- likes
- comments
- shares
- saves
- impressions
- reach

## DAILY_SUMMARY
- id (uuid)
- social_account_id
- date
- followers
- new_followers
- posts_count
- total_likes
- total_comments
- engagement_rate

## AI_INSIGHTS
- id (uuid)
- social_account_id
- generated_at
- insight_type (best_time, content_idea, audience)
- text
- metadata_json

INITIAL PLATFORM:
- Start with ONE platform first: `platform = "instagram"` (or "twitter") and extend later.

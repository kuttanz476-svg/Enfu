# ENFU ANALYTICS — API DESIGN (MINIMUM VIABLE)

Base URL example: `/api/v1`

## AUTH
### POST /auth/signup
- Input: email, password
- Output: user info + JWT token

### POST /auth/login
- Input: email, password
- Output: JWT token

## SOCIAL ACCOUNTS
### POST /social-accounts/connect
- Input: platform, auth_code (from OAuth)
- Action: exchange code for token, save account
- Output: social_account object

### GET /social-accounts
- Output: list of connected accounts

## SYNC
### POST /social-accounts/{id}/sync
- Action: fetch latest posts + stats from platform API
- Output: status (started / completed)

## DASHBOARD
### GET /dashboard/overview?social_account_id=...
- Output:
  - follower_count
  - follower_growth_7d
  - engagement_rate_7d
  - top_posts (3–5 posts with stats)

### GET /dashboard/top-posts?social_account_id=...
- Output: list of posts sorted by engagement

## AI INSIGHTS
### GET /insights?social_account_id=...
- Output:
  - best_posting_times[]
  - content_suggestions[]
  - notes_about_audience[]

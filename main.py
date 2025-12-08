from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "enfu-backend"}

@app.get("/dashboard/fake")
def fake_dashboard():
    return {
        "followers": 1200,
        "engagement_rate": 3.8,
        "top_posts": [
            {"id": 1, "likes": 220, "comments": 14},
            {"id": 2, "likes": 195, "comments": 10},
            {"id": 3, "likes": 180, "comments": 9}
        ]
    }

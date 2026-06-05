from fastapi import FastAPI
from app.routes.feed_routes import router as feed_router

app = FastAPI(
    title="Feed Service",
    description="Generates user feeds from follow and post services",
    version="1.0.0"
)

app.include_router(feed_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "feed-service"}
from fastapi import FastAPI
from app.routes.post_routes import router as post_router

app = FastAPI(
    title="Post Service",
    description="Handles post creation and retrieval",
    version="1.0.0"
)

app.include_router(post_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "post-service"}
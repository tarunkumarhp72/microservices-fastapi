from fastapi import FastAPI
from app.routes.follow_routes import router

app = FastAPI(
    title="Follow Service",
    description="Manages follow/unfollow relationships",
    version="1.0.0"
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "follow-service"}
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI
from app.api.v1.post_routes import router as post_router
from shared_lib.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared_lib.logger import setup_logger
from shared_lib.exceptions import register_exception_handlers

logger = setup_logger(service_name="post-microservice")

app = FastAPI(
    title="Post Service",
    description="Handles post creation and retrieval",
    version="1.0.0"
)
app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)

app.include_router(post_router)

@app.on_event("startup")
async def startup():
    logger.info("Post service started", extra={"port": 8003})

@app.get("/health")
def health():
    return {"status": "ok", "service": "post-service"}
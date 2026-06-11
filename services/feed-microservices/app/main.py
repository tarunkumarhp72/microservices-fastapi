import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE_DIR))
from fastapi import FastAPI
import fastapi

import sys
from pathlib import Path
from app.api.v1.feed_routes import router as feed_router
from shared_lib.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared_lib.logger import setup_logger
from shared_lib.exceptions import register_exception_handlers
logger = setup_logger(service_name="feed-microservice")


app = FastAPI(
    title="Feed Service",
    description="Generates user feeds from follow and post services",
    version="1.0.0"
)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)

app.include_router(feed_router)

@app.on_event("startup")
async def startup():
    logger.info("Feed service started", extra={"port": 8004})

@app.get("/health")
def health():
    return {"status": "ok", "service": "feed-microservice"}
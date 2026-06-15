
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.feed_routes import router as feed_router
from shared.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared.logger import setup_logger
from shared.exceptions import register_exception_handlers

logger = setup_logger(service_name="feed-microservice")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Feed service started",
        extra={"port": 8004}
    )

    yield

    logger.info(
        "Feed service shutting down",
        extra={"port": 8004}
    )


app = FastAPI(
    title="Feed Service",
    description="Generates user feeds from follow and post services",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)

register_exception_handlers(app)

app.include_router(feed_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "feed-microservice"
    }
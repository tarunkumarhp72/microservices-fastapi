
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.post_routes import router as post_router
from shared.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared.logger import setup_logger
from shared.exceptions import register_exception_handlers
from app.database import Base, engine

logger = setup_logger(service_name="post-microservice")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)   
    logger.info(
        "Post service started",
        extra={"port": 8003}
    )

    yield

    logger.info(
        "Post service shutting down",
        extra={"port": 8003}
    )


app = FastAPI(
    title="Post Service",
    description="Handles post creation and retrieval",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)

register_exception_handlers(app)

app.include_router(post_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "post-service"
    }
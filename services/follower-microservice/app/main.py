
from contextlib import asynccontextmanager
from fastapi import FastAPI


from app.api.v1.follow_routes import router
from app.database import Base, engine
from shared.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared.logger import setup_logger
from shared.exceptions import register_exception_handlers

logger = setup_logger(service_name="follow-microservice")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Follow service started",
        extra={"port": 8002}
    )

    yield

    logger.info(
        "Follow service shutting down",
        extra={"port": 8002}
    )


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Follow Service",
    description="Manages follow/unfollow relationships",
    version="1.0.0",
    lifespan=lifespan
)

register_exception_handlers(app)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "follow-service"
    }
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE_DIR))




from fastapi import FastAPI
from app.api.v1.follow_routes import router
from app.database import Base, engine
from shared_lib.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared_lib.logger import setup_logger
from shared_lib.exceptions import register_exception_handlers

logger = setup_logger(service_name="follow-microservice")

Base.metadata.create_all(bind=engine) 
app = FastAPI(
    title="Follow Service",
    description="Manages follow/unfollow relationships",
    version="1.0.0"
)
register_exception_handlers(app)
app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(RequestIDMiddleware)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "follow-service"}
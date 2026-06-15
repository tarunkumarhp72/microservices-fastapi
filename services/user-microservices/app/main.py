

from fastapi import FastAPI

from .database import Base
from .database import ensure_user_schema
from .database import engine
from shared.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared.exceptions import register_exception_handlers


from app.api.v1.user_routes import router as user_router
from shared.logger import setup_logger
from app.models.user_model import User 

logger = setup_logger(service_name="user-microservice")


app = FastAPI(
    title="User Microservice"
)


app.add_middleware(ProcessTimeMiddleware)

app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)


app.include_router(user_router)


Base.metadata.create_all(bind=engine) 
@app.on_event("startup")
async def startup():
    ensure_user_schema()
    logger.info("User service started", extra={"port": 8001})
 
 
@app.on_event("shutdown")
async def shutdown():
    logger.info("User service shutting down")




@app.get("/health")
def health():
    return {"status": "ok"}

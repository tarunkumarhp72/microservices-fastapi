import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE_DIR))


from fastapi import FastAPI

from app.database import Base
from app.database import engine
from shared_lib.middleware import RequestIDMiddleware, ProcessTimeMiddleware
from shared_lib.exceptions import register_exception_handlers


from app.api.v1.user_routes import router as user_router
from shared_lib.logger import setup_logger


logger = setup_logger(service_name="user-microservice")


app = FastAPI(
    title="User Microservice"
)


app.add_middleware(ProcessTimeMiddleware)

app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)


app.include_router(user_router)



@app.on_event("startup")
async def startup():
    logger.info("User service started", extra={"port": 8001})
 
 
@app.on_event("shutdown")
async def shutdown():
    logger.info("User service shutting down")




@app.get("/")
def health_check():
    return {
        "status": "running"
    }
from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routes.user_routes import router as user_router
from app.routes.follow_routes import router as follow_routes 
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service"
)

app.include_router(user_router)
app.include_router(follow_routes)   


@app.get("/")
def health_check():
    return {
        "status": "running"
    }
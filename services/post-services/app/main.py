from app.routes.post_routes import router as post_router
from fastapi import FastAPI


app = FastAPI(
    title="Post Service"
)

app.include_router(post_router)
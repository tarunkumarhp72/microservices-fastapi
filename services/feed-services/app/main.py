from fastapi import FastAPI

from app.routes.feed_routes import router as feed_router


app = FastAPI()

app.include_router(feed_router)
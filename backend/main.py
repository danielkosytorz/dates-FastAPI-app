import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.settings import settings
from src.dates.routers.routers import dates, popular

app = FastAPI()
app.include_router(dates)
app.include_router(popular)

register_tortoise(
    app,
    db_url=(
        f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    ),
    modules=settings.APP_MODELS,
    add_exception_handlers=True,
)

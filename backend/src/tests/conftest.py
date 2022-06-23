import asyncio
import os
from asyncio import AbstractEventLoop

import pytest
from httpx import AsyncClient
from tortoise import Tortoise, generate_schema_for_client

from main import app
from src.settings import settings


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


TORTOISE_ORM_TEST = settings.TORTOISE_ORM
TORTOISE_ORM_TEST["connections"] = {
    "default": (
        f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/test_database"
    )
}


@pytest.fixture(scope="function", autouse=True)
async def initialize_db():
    await Tortoise.init(config=TORTOISE_ORM_TEST, _create_db=True)
    await generate_schema_for_client(Tortoise.get_connection("default"), safe=True)
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8008") as async_client:
        yield async_client

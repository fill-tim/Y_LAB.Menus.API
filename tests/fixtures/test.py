from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from app.models import Dish, Menu, Submenu
from ..db import engine_test, Base, async_session_maker, override_get_redis
from ..conftest import app


@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        redis = await override_get_redis()
        await redis.flushall()


@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def init_default_data():
    async with async_session_maker() as db:
        test_menu_default = Menu(title="My menu 1", description="My menu description 1")

        db.add(test_menu_default)
        await db.commit()

        test_submenu_default = Submenu(
            title="My submenu 1",
            description="My submenu description 1",
            menu_id=test_menu_default.id,
        )

        db.add(test_submenu_default)
        await db.commit()

        test_dish_default = Dish(
            title="My dish 1",
            description="My dish description 1",
            price="123.12",
            submenu_id=test_submenu_default.id,
        )

        db.add(test_dish_default)
        await db.commit()

        return {
            "test_menu_default": test_menu_default,
            "test_submenu_default": test_submenu_default,
            "test_dish_default": test_dish_default,
        }

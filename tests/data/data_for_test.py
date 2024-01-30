import pytest
from tests import Menu, Submenu, Dish
from conftest import async_session_maker


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

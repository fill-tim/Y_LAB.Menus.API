from httpx import AsyncClient
import pytest
from conftest import async_session_maker
from tests import Menu


@pytest.mark.asyncio(scope="session")
async def test_list_menus_success(ac: AsyncClient):
    async with async_session_maker() as db:
        test_menu_1 = Menu(title="My menu 1", description="My menu description 1")
        test_menu_2 = Menu(title="My menu 2", description="My menu description 2")

        db.add_all([test_menu_1, test_menu_2])
        await db.commit()

    test_menu_1_id = test_menu_1.id
    test_menu_2_id = test_menu_2.id

    response = await ac.get(f"api/v1/menus")

    assert response.status_code == 200
    assert {
        "id": str(test_menu_1_id),
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0,
    } in response.json()

    assert {
        "id": str(test_menu_2_id),
        "title": "My menu 2",
        "description": "My menu description 2",
        "submenus_count": 0,
        "dishes_count": 0,
    } in response.json()

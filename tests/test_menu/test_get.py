from httpx import AsyncClient
import pytest
from conftest import async_session_maker
from tests import Menu
import uuid


@pytest.mark.asyncio(scope="session")
async def test_get_menu_success(ac: AsyncClient):
    async with async_session_maker() as db:
        test_menu = Menu(title="My menu 1", description="My menu description 1")

        db.add(test_menu)
        await db.commit()
        await db.refresh(test_menu)

    test_menu_id = test_menu.id

    response = await ac.get(f"api/v1/menus/{test_menu_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_menu_id),
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0,
    }


@pytest.mark.asyncio(scope="session")
async def test_get_menu_failed(ac: AsyncClient):
    async with async_session_maker() as db:
        test_menu = Menu(title="My menu 1", description="My menu description 1")

        db.add(test_menu)
        await db.commit()
        await db.refresh(test_menu)

    test_menu_id = uuid.uuid4()

    response = await ac.get(f"api/v1/menus/{test_menu_id}")

    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

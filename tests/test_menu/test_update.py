from httpx import AsyncClient
import pytest
from conftest import async_session_maker
from tests import Menu
import uuid


@pytest.mark.asyncio(scope="session")
async def test_update_menu_success(ac: AsyncClient):
    async with async_session_maker() as db:
        test_menu = Menu(title="My menu 1", description="My menu description 1")

        db.add(test_menu)
        await db.commit()
        await db.refresh(test_menu)

    test_menu_id = test_menu.id

    response = await ac.patch(
        f"api/v1/menus/{test_menu_id}",
        json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_menu_id),
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }


@pytest.mark.asyncio(scope="session")
async def test_update_menu_failed(ac: AsyncClient):
    async with async_session_maker() as db:
        test_menu = Menu(title="My menu 1", description="My menu description 1")

        db.add(test_menu)
        await db.commit()
        await db.refresh(test_menu)

    test_menu_id = uuid.uuid4()

    response = await ac.patch(
        f"api/v1/menus/{test_menu_id}",
        json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "menu not found"
    }

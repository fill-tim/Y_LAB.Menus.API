from httpx import AsyncClient
import pytest
from conftest import async_session_maker
from tests import Menu
import uuid


@pytest.mark.asyncio(scope="session")
async def test_delete_menu_success(ac: AsyncClient):
    async with async_session_maker() as db:
        test_menu = Menu(title="My menu 1", description="My menu description 1")

        db.add(test_menu)
        await db.commit()
        await db.refresh(test_menu)

    test_menu_id = test_menu.id

    response = await ac.delete(f"api/v1/menus/{test_menu_id}")

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The menu has been deleted"
    }

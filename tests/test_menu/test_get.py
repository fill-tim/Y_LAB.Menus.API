from httpx import AsyncClient
import pytest
from conftest import async_session_maker
from tests import Menu
import uuid
from data.data_for_test import DataForTests


@pytest.mark.asyncio
async def test_get_menu_success(ac: AsyncClient):
    data = await DataForTests.init_default_data()

    test_menu_id = data["test_menu_default"].id

    response = await ac.get(f"api/v1/menus/{test_menu_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_menu_id),
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 1,
        "dishes_count": 1,
    }


@pytest.mark.asyncio
async def test_get_menu_failed(ac: AsyncClient):
    test_menu_id = uuid.uuid4()

    response = await ac.get(f"api/v1/menus/{test_menu_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

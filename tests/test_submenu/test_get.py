from httpx import AsyncClient
import pytest
from data.data_for_test import init_default_data
import uuid


@pytest.mark.asyncio
async def test_get_submenu_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id

    response = await ac.get(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}", 
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_submenu_id),
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 1,
    }


@pytest.mark.asyncio
async def test_get_submenu_failed(ac: AsyncClient):
    test_menu_id = uuid.uuid4()
    test_submenu_id = uuid.uuid4()

    response = await ac.get(f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}

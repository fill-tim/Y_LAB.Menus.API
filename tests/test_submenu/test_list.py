from httpx import AsyncClient
import pytest
from data.data_for_test import init_default_data


@pytest.mark.asyncio
async def test_list_submenus_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id

    response = await ac.get(f"api/v1/menus/{test_menu_id}/submenus")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {
        "id": str(test_submenu_id),
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 1,
    } in response.json()


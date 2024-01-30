from httpx import AsyncClient
import pytest
from data.data_for_test import init_default_data


@pytest.mark.asyncio
async def test_list_menus_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id

    response = await ac.get(f"api/v1/menus")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {
        "id": str(test_menu_id),
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 1,
        "dishes_count": 1,
    } in response.json()

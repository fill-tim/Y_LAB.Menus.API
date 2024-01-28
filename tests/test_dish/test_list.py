from httpx import AsyncClient
import pytest
from data.data_for_test import DataForTests


@pytest.mark.asyncio
async def test_list_dihes_success(ac: AsyncClient):
    data = await DataForTests.init_default_data()

    test_menu_id = data["test_menu_default"].id
    test_submenu_id = data["test_submenu_default"].id
    test_dish_id = data["test_dish_default"].id
    
    response = await ac.get(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}/dishes"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {
        "id": str(test_dish_id),
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "123.12",
    } in response.json()

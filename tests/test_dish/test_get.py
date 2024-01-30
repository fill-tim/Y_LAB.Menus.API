from httpx import AsyncClient
import pytest
import uuid
from data.data_for_test import init_default_data


@pytest.mark.asyncio
async def test_get_dish_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id
    test_dish_id = init_default_data["test_dish_default"].id

    response = await ac.get(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}/dishes/{test_dish_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_dish_id),
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "123.12",
    }


@pytest.mark.asyncio
async def test_get_submenu_failed(ac: AsyncClient):
    test_menu_id = uuid.uuid4()
    test_submenu_id = uuid.uuid4()
    test_dish_id = uuid.uuid4()

    response = await ac.get(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}/dishes/{test_dish_id}",
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}

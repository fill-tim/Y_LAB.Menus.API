from httpx import AsyncClient
import pytest
import uuid
from data.data_for_test import init_default_data


@pytest.mark.asyncio
async def test_update_dish_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id

    response = await ac.patch(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}",
        json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_submenu_id),
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
    }


@pytest.mark.asyncio
async def test_update_dish_failed(ac: AsyncClient):
    test_menu_id = uuid.uuid4()
    test_submenu_id = uuid.uuid4()

    response = await ac.patch(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}",
        json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


@pytest.mark.asyncio
async def test_update_dish_failed_title(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id

    response = await ac.patch(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}",
        json={
            "title": 123,
            "description": "My updated submenu description 1",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


@pytest.mark.asyncio
async def test_update_dish_failed_description(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id

    response = await ac.patch(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}",
        json={
            "title": "My updated submenu 1",
            "description": 123,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

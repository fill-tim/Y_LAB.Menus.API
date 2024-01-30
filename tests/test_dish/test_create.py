from httpx import AsyncClient
import pytest
from data.data_for_test import init_default_data


@pytest.mark.asyncio
async def test_create_dish_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id

    response = await ac.post(
        f"api/v1/menus/{test_menu_id}/submenus",
        json={
            "title": "My new submenu 1",
            "description": "My new submenu description 1",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] != ""
    assert response.json()["title"] == "My new submenu 1"
    assert response.json()["description"] == "My new submenu description 1"


@pytest.mark.asyncio
async def test_create_dish_failed_title(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id

    response = await ac.post(
        f"api/v1/menus/{test_menu_id}/submenus",
        json={
            "title": 123,
            "description": "My new submenu description 1",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


@pytest.mark.asyncio
async def test_create_dish_failed_description(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id

    response = await ac.post(
        f"api/v1/menus/{test_menu_id}/submenus",
        json={
            "title": "My new submenu 1",
            "description": 123,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"




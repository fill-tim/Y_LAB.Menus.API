from httpx import AsyncClient
import pytest
from data.data_for_test import DataForTests


@pytest.mark.asyncio
async def test_create_submenu_success(ac: AsyncClient):
    data = await DataForTests.init_default_data()

    test_menu_id = data["test_menu_default"].id

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
async def test_create_submenu_failed_title(ac: AsyncClient):
    data = await DataForTests.init_default_data()

    test_menu_id = data["test_menu_default"].id

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
async def test_create_submenu_failed_description(ac: AsyncClient):
    data = await DataForTests.init_default_data()

    test_menu_id = data["test_menu_default"].id

    response = await ac.post(
        f"api/v1/menus/{test_menu_id}/submenus",
        json={
            "title": "My new submenu 1",
            "description": 123,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

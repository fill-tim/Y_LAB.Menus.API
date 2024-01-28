from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_menu_success(ac: AsyncClient):
    response = await ac.post(
        f"api/v1/menus",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )

    assert response.status_code == 201
    assert response.json()["id"] != ""
    assert response.json()["title"] == "My menu 1"
    assert response.json()["description"] == "My menu description 1"


@pytest.mark.asyncio
async def test_create_menu_failed_title(ac: AsyncClient):
    response = await ac.post(
        f"api/v1/menus",
        json={"title": 123, "description": "My menu description 1"},
    )
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


@pytest.mark.asyncio
async def test_create_menu_failed_title(ac: AsyncClient):
    response = await ac.post(
        f"api/v1/menus",
        json={"title": "My menu 1", "description": 123},
    )
   
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

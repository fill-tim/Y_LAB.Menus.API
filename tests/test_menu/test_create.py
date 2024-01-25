from httpx import AsyncClient
import pytest


@pytest.mark.asyncio(scope="session")
async def test_create_menu_completed_success(ac: AsyncClient):
    response = await ac.post(
        f"api/v1/menus",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )

    assert response.status_code == 201
    assert response.json()["id"] != ""
    assert response.json()["title"] == "My menu 1"
    assert response.json()["description"] == "My menu description 1"

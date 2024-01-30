from httpx import AsyncClient
import pytest
from uuid import uuid4
from data.data_for_test import init_default_data


@pytest.mark.asyncio
async def test_delete_submenu_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id

    response = await ac.delete(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The submenu has been deleted",
    }


@pytest.mark.asyncio
async def test_delete_submenu_failed(ac: AsyncClient):
    test_menu_id = uuid4()
    test_submenu_id = uuid4()

    response = await ac.delete(
        f"api/v1/menus/{test_menu_id}/submenus/{test_submenu_id}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}

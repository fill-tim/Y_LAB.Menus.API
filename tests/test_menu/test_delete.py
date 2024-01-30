from httpx import AsyncClient
import pytest
from data.data_for_test import init_default_data
from uuid import uuid4


@pytest.mark.asyncio
async def test_delete_menu_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data["test_menu_default"].id

    response = await ac.delete(f"api/v1/menus/{test_menu_id}")

    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "The menu has been deleted"}


@pytest.mark.asyncio
async def test_delete_menu_failed(ac: AsyncClient):
    test_menu_id = uuid4()

    response = await ac.delete(f"api/v1/menus/{test_menu_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

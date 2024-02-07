from uuid import uuid4

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_delete_dish_success(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data["test_menu_default"].id
    test_submenu_id = init_default_data["test_submenu_default"].id
    test_dish_id = init_default_data["test_dish_default"].id

    url = await reverse_url(
        "delete_dish",
        menu_id=test_menu_id,
        submenu_id=test_submenu_id,
        dish_id=test_dish_id,
    )

    response = await ac.delete(url)

    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "The dish has been deleted",
    }


async def test_delete_submenu_failed(ac: AsyncClient) -> None:
    test_menu_id = uuid4()
    test_submenu_id = uuid4()
    test_dish_id = uuid4()

    url = await reverse_url(
        "delete_dish",
        menu_id=test_menu_id,
        submenu_id=test_submenu_id,
        dish_id=test_dish_id,
    )

    response = await ac.delete(url)

    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}

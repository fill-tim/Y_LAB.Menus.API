import uuid

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_update_menu_success(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data["test_menu_default"].id

    url = await reverse_url("update_menu", menu_id=test_menu_id)

    response = await ac.patch(
        url,
        json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_menu_id),
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
        "dishes_count": 1,
        "submenus_count": 1,
    }


async def test_update_menu_failed_title(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data["test_menu_default"].id

    url = await reverse_url("update_menu", menu_id=test_menu_id)

    response = await ac.patch(
        url,
        json={
            "title": 123,
            "description": "My updated menu description 1",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


async def test_update_menu_failed_description(
    ac: AsyncClient, init_default_data
) -> None:
    test_menu_id = init_default_data["test_menu_default"].id

    url = await reverse_url("update_menu", menu_id=test_menu_id)

    response = await ac.patch(
        url,
        json={
            "title": "My updated menu 1",
            "description": 123,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


async def test_update_menu_failed(ac: AsyncClient) -> None:
    test_menu_id = uuid.uuid4()

    url = await reverse_url("update_menu", menu_id=test_menu_id)

    response = await ac.patch(
        url,
        json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_check_the_number_of_dishes_and_submenus_in_menu(ac: AsyncClient):
    created_menu = await ac.post(
        f"api/v1/menus",
        json={"title": "My menu 1", "description": "My menu description 1"},
    )

    assert created_menu.status_code == 201
    assert created_menu.json()["id"] != ""
    assert created_menu.json()["title"] == "My menu 1"
    assert created_menu.json()["description"] == "My menu description 1"

    menu_id = created_menu.json()["id"]

    created_submenu = await ac.post(
        f"api/v1/menus/{menu_id}/submenus",
        json={"title": "My submenu 1", "description": "My submenu description 1"},
    )

    assert created_submenu.status_code == 201
    assert created_submenu.json()["id"] != ""
    assert created_submenu.json()["title"] == "My submenu 1"
    assert created_submenu.json()["description"] == "My submenu description 1"

    submenu_id = created_submenu.json()["id"]

    created_first_dish = await ac.post(
        f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "123.32",
        },
    )

    assert created_first_dish.status_code == 201
    assert created_first_dish.json()["id"] != ""
    assert created_first_dish.json()["title"] == "My dish 1"
    assert created_first_dish.json()["description"] == "My dish description 1"

    created_second_dish = await ac.post(
        f"api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json={
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": "123.32",
        },
    )

    assert created_second_dish.status_code == 201
    assert created_second_dish.json()["id"] != ""
    assert created_second_dish.json()["title"] == "My dish 2"
    assert created_second_dish.json()["description"] == "My dish description 2"

    menu = await ac.get(
        f"api/v1/menus/{menu_id}",
    )

    assert menu.status_code == 200
    assert menu.json()["id"] == menu_id
    assert menu.json()["title"] == "My menu 1"
    assert menu.json()["description"] == "My menu description 1"
    assert menu.json()["submenus_count"] == 1
    assert menu.json()["dishes_count"] == 2

    submenu = await ac.get(
        f"api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )

    assert submenu.status_code == 200
    assert submenu.json()["id"] == submenu_id
    assert submenu.json()["title"] == "My submenu 1"
    assert submenu.json()["description"] == "My submenu description 1"
    assert submenu.json()["dishes_count"] == 2

    deleted_submenu = await ac.delete(
        f"api/v1/menus/{menu_id}/submenus/{submenu_id}",
    )

    assert deleted_submenu.status_code == 200
    assert deleted_submenu.json() == {
        "status": True,
        "message": "The submenu has been deleted",
    }

    list_submenu = await ac.get(
        f"api/v1/menus/{menu_id}/submenus",
    )

    assert list_submenu.status_code == 200
    assert list_submenu.json() == []

    list_dishes = await ac.get(
        f"api/v1/menus/{menu_id}/submenus",
    )

    assert list_dishes.status_code == 200
    assert list_dishes.json() == []

    specific_submenu = await ac.get(
        f"api/v1/menus/{menu_id}",
    )

    assert specific_submenu.status_code == 200
    assert specific_submenu.json()["id"] == menu_id
    assert specific_submenu.json()["title"] == "My menu 1"
    assert specific_submenu.json()["description"] == "My menu description 1"
    assert specific_submenu.json()["dishes_count"] == 0

    deleted_menu = await ac.delete(
        f"api/v1/menus/{menu_id}",
    )

    assert deleted_menu.status_code == 200
    assert deleted_menu.json() == {
        "status": True,
        "message": "The menu has been deleted",
    }

    specific_menu = await ac.get(
        f"api/v1/menus",
    )

    assert specific_menu.status_code == 200
    assert specific_menu.json() == []

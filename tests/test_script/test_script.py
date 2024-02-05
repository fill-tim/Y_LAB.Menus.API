import pytest
from httpx import AsyncClient
from ..helpers import reverse_url


@pytest.mark.asyncio
async def test_check_the_number_of_dishes_and_submenus_in_menu(ac: AsyncClient):
    create_menu_url = await reverse_url("create")

    created_menu = await ac.post(
        create_menu_url,
        json={"title": "My menu 1", "description": "My menu description 1"},
    )

    assert created_menu.status_code == 201
    assert created_menu.json()["id"] != ""
    assert created_menu.json()["title"] == "My menu 1"
    assert created_menu.json()["description"] == "My menu description 1"

    menu_id = created_menu.json()["id"]

    create_submenu_url = await reverse_url("create", menu_id=menu_id)

    created_submenu = await ac.post(
        create_submenu_url,
        json={"title": "My submenu 1", "description": "My submenu description 1"},
    )

    assert created_submenu.status_code == 201
    assert created_submenu.json()["id"] != ""
    assert created_submenu.json()["title"] == "My submenu 1"
    assert created_submenu.json()["description"] == "My submenu description 1"

    submenu_id = created_submenu.json()["id"]

    create_first_dish_url = await reverse_url(
        "create", menu_id=menu_id, submenu_id=submenu_id
    )

    created_first_dish = await ac.post(
        create_first_dish_url,
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

    create_second_dish_url = await reverse_url(
        "create", menu_id=menu_id, submenu_id=submenu_id
    )

    created_second_dish = await ac.post(
        create_second_dish_url,
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

    menu_url = await reverse_url("get", id=menu_id)
    
    menu = await ac.get(menu_url)

    assert menu.status_code == 200
    assert menu.json()["id"] == menu_id
    assert menu.json()["title"] == "My menu 1"
    assert menu.json()["description"] == "My menu description 1"
    assert menu.json()["submenus_count"] == 1
    assert menu.json()["dishes_count"] == 2

    submenu_url = await reverse_url("get", menu_id=menu_id, id=submenu_id)
    
    submenu = await ac.get(submenu_url)

    assert submenu.status_code == 200
    assert submenu.json()["id"] == submenu_id
    assert submenu.json()["title"] == "My submenu 1"
    assert submenu.json()["description"] == "My submenu description 1"
    assert submenu.json()["dishes_count"] == 2

    delete_submenu_url = await reverse_url(
        "delete", menu_id=menu_id, id=submenu_id
    )

    deleted_submenu = await ac.delete(delete_submenu_url)

    assert deleted_submenu.status_code == 200
    assert deleted_submenu.json() == {
        "status": True,
        "message": "The submenu has been deleted",
    }

    list_submenu_url = await reverse_url("list", menu_id=menu_id)
    
    list_submenu = await ac.get(list_submenu_url)

    assert list_submenu.status_code == 200
    assert list_submenu.json() == []

    list_dish_url = await reverse_url("list", menu_id=menu_id, submenu_id=submenu_id)

    list_dishes = await ac.get(list_dish_url)

    assert list_dishes.status_code == 200
    assert list_dishes.json() == []

    specific_menu_url = await reverse_url("get", id=menu_id)

    specific_menu = await ac.get(specific_menu_url)

    assert specific_menu.status_code == 200
    assert specific_menu.json()["id"] == menu_id
    assert specific_menu.json()["title"] == "My menu 1"
    assert specific_menu.json()["description"] == "My menu description 1"
    assert specific_menu.json()["submenus_count"] == 0
    assert specific_menu.json()["dishes_count"] == 0

    delete_menu_url = await reverse_url("delete", id=menu_id)

    deleted_menu = await ac.delete(delete_menu_url)

    assert deleted_menu.status_code == 200
    assert deleted_menu.json() == {
        "status": True,
        "message": "The menu has been deleted",
    }

    list_menu_url = await reverse_url("list")

    specific_menus = await ac.get(list_menu_url)

    assert specific_menus.status_code == 200
    assert specific_menus.json() == []

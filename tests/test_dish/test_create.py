from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_create_dish_success(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('create_dish', menu_id=test_menu_id, submenu_id=test_submenu_id)

    response = await ac.post(
        url,
        json={
            'title': 'My new dish 1',
            'description': 'My new dish description 1',
            'price': '123.234',
        },
    )

    assert response.status_code == 201
    assert response.json()['id'] != ''
    assert response.json()['title'] == 'My new dish 1'
    assert response.json()['description'] == 'My new dish description 1'
    assert response.json()['price'] == '123.23'


async def test_create_dish_failed_title(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('create_dish', menu_id=test_menu_id, submenu_id=test_submenu_id)

    response = await ac.post(
        url,
        json={
            'title': 123,
            'description': 'My new dish description 1',
            'price': '123.234',
        },
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'


async def test_create_dish_failed_description(
    ac: AsyncClient, init_default_data
) -> None:
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('create_dish', menu_id=test_menu_id, submenu_id=test_submenu_id)

    response = await ac.post(
        url,
        json={
            'title': 'My new submenu 1',
            'description': 123,
            'price': '123.234',
        },
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'

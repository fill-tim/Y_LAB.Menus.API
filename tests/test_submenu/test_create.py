from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_create_submenu_success(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data['test_menu_default'].id

    url = await reverse_url('create_submenu', menu_id=test_menu_id)

    response = await ac.post(
        url,
        json={
            'title': 'My new submenu 1',
            'description': 'My new submenu description 1',
        },
    )

    assert response.status_code == 201
    assert response.json()['id'] != ''
    assert response.json()['title'] == 'My new submenu 1'
    assert response.json()['description'] == 'My new submenu description 1'


async def test_create_submenu_failed_title(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data['test_menu_default'].id

    url = await reverse_url('create_submenu', menu_id=test_menu_id)

    response = await ac.post(
        url,
        json={
            'title': 123,
            'description': 'My new submenu description 1',
        },
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'


async def test_create_submenu_failed_description(
    ac: AsyncClient, init_default_data
) -> None:
    test_menu_id = init_default_data['test_menu_default'].id

    url = await reverse_url('create_submenu', menu_id=test_menu_id)

    response = await ac.post(
        url,
        json={
            'title': 'My new submenu 1',
            'description': 123,
        },
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'

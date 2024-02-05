import uuid

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_update_submenu_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('update', menu_id=test_menu_id, id=test_submenu_id)

    response = await ac.patch(
        url,
        json={
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': str(test_submenu_id),
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
        'dishes_count': 1,
    }


async def test_update_submenu_failed(ac: AsyncClient):
    test_menu_id = uuid.uuid4()
    test_submenu_id = uuid.uuid4()

    url = await reverse_url('update', menu_id=test_menu_id, id=test_submenu_id)

    response = await ac.patch(
        url,
        json={
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1',
        },
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


async def test_update_submenu_failed_title(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('update', menu_id=test_menu_id, id=test_submenu_id)

    response = await ac.patch(
        url,
        json={
            'title': 123,
            'description': 'My updated submenu description 1',
        },
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'


async def test_update_submenu_failed_description(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('update', menu_id=test_menu_id, id=test_submenu_id)

    response = await ac.patch(
        url,
        json={
            'title': 'My updated submenu 1',
            'description': 123,
        },
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'

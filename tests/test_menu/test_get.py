import uuid

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_get_menu_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id

    url = await reverse_url('get', id=test_menu_id)

    response = await ac.get(url)

    assert response.status_code == 200
    assert response.json() == {
        'id': str(test_menu_id),
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 1,
        'dishes_count': 1,
    }


async def test_get_menu_failed(ac: AsyncClient):
    test_menu_id = uuid.uuid4()

    url = await reverse_url('get', id=test_menu_id)

    response = await ac.get(url)

    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}

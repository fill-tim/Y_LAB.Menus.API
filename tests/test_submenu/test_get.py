import uuid

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_get_submenu_success(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('get_submenu', menu_id=test_menu_id, submenu_id=test_submenu_id)

    response = await ac.get(url)

    assert response.status_code == 200
    assert response.json() == {
        'id': str(test_submenu_id),
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'dishes_count': 1,
    }


async def test_get_submenu_failed(ac: AsyncClient) -> None:
    test_menu_id = uuid.uuid4()
    test_submenu_id = uuid.uuid4()

    url = await reverse_url('get_submenu', menu_id=test_menu_id, submenu_id=test_submenu_id)

    response = await ac.get(url)

    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_list_menus_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id

    url = await reverse_url('list')

    response = await ac.get(url)
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {
        'id': str(test_menu_id),
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 1,
        'dishes_count': 1,
    } in response.json()

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_list_submenus_success(ac: AsyncClient, init_default_data) -> None:
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id

    url = await reverse_url('list_submenu', menu_id=test_menu_id)

    response = await ac.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {
        'id': str(test_submenu_id),
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'dishes_count': 1,
    } in response.json()

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_list_dihes_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id
    test_submenu_id = init_default_data['test_submenu_default'].id
    test_dish_id = init_default_data['test_dish_default'].id

    url = await reverse_url('list', menu_id=test_menu_id, submenu_id=test_submenu_id)

    response = await ac.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {
        'id': str(test_dish_id),
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '123.12',
    } in response.json()

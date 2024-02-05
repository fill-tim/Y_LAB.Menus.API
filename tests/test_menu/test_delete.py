from uuid import uuid4

from httpx import AsyncClient

from ..helpers.create_url import reverse_url


async def test_delete_menu_success(ac: AsyncClient, init_default_data):
    test_menu_id = init_default_data['test_menu_default'].id

    url = await reverse_url('delete', id=test_menu_id)
    
    response = await ac.delete(url)

    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


async def test_delete_menu_failed(ac: AsyncClient):
    test_menu_id = uuid4()

    url = await reverse_url('delete', id=test_menu_id)

    response = await ac.delete(url)

    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}

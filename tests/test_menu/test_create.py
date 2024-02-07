from httpx import AsyncClient

from ..helpers.create_url import reverse_url


class TestCreateMenu:
    async def test_create_menu_success(self, ac: AsyncClient) -> None:
        url = await reverse_url('create_menu')

        response = await ac.post(
            url,
            json={'title': 'My menu 1', 'description': 'My menu description 1'},
        )

        assert response.status_code == 201
        assert response.json()['id'] != ''
        assert response.json()['title'] == 'My menu 1'
        assert response.json()['description'] == 'My menu description 1'

    async def test_create_menu_failed_title(self, ac: AsyncClient) -> None:
        url = await reverse_url('create_menu')

        response = await ac.post(
            url,
            json={'title': 123, 'description': 'My menu description 1'},
        )

        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'

    async def test_create_menu_failed_description(self, ac: AsyncClient) -> None:
        url = await reverse_url('create_menu')

        response = await ac.post(
            url,
            json={'title': 'My menu 1', 'description': 123},
        )

        assert response.status_code == 422
        assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'

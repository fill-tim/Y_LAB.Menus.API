from uuid import UUID

from ..conftest import app


async def reverse_url(name: str, **kwargs: str | UUID) -> str:

    url = ''

    for route in app.routes:
        if route.name == name:
            url = route.path

    if url == '0':
        raise ValueError(f'Нет роутера с name{name}')

    # for param, value in kwargs.items():
    #     if param:
    #         for item in urls_routers_equal_name[::-1]:
    #             if param in item:
    #                 url = item

    for param, value in kwargs.items():
        url = url.replace(f'{{{param}}}', str(value))

    return url

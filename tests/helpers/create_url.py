from uuid import UUID

from ..conftest import app


async def reverse_url(name: str, **kwargs: UUID) -> str:
    return app.url_path_for(name, **kwargs)

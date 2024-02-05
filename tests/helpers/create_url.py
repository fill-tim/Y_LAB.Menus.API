from ..conftest import app
from uuid import UUID


async def reverse_url(name: str, **kwargs: UUID) -> str:
    return app.url_path_for(name, **kwargs)

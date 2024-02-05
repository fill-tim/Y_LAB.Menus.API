from app.core.db import get_async_session
from app.core.redis import get_redis
from app.main import app

from .db import override_get_async_session, override_get_redis
from .fixtures import ac, init_default_data, prepare_database

app.dependency_overrides[get_async_session] = override_get_async_session
app.dependency_overrides[get_redis] = override_get_redis

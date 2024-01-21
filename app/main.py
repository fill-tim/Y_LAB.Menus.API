from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api import menu_router, submenu_router, dish_router
from .models import Base
from .core import engine

from . import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield
    except Exception as error:
        print(error)


app = FastAPI(lifespan=lifespan)


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)

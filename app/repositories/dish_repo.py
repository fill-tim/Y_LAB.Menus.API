from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from uuid import UUID

from ..schemas.dish_schemas import DishAdd
from app.models import Dish
from app.repositories import BaseRepo


class DishRepo(BaseRepo):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        super().__init__(model=Dish, db=db)

    async def create(self, dish_in: DishAdd, submenu_id: UUID):
        try:
            price = round(float(dish_in.price), 2)
            dish_in.price = str(price)
            
            obj = Dish(**dish_in.model_dump(), submenu_id=submenu_id)

            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)

            return obj
        except Exception as error:
            return error

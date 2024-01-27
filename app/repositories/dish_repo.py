from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from uuid import UUID
from sqlalchemy import select
from ..schemas.dish_schemas import DishAdd
from app.models import Dish
from app.repositories import BaseRepo


class DishRepo(BaseRepo):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        super().__init__(model=Dish, db=db)

    async def get_all(self, submenu_id: UUID):
        dishes = await self.db.execute(
            select(Dish).where(Dish.submenu_id == submenu_id)
        )

        return list(dishes.scalars())

    async def create(self, dish_in: DishAdd, submenu_id: UUID):
        price = round(float(dish_in.price), 2)
        dish_in.price = str(price)

        dish = Dish(**dish_in.model_dump(), submenu_id=submenu_id)

        self.db.add(dish)
        await self.db.commit()
        await self.db.refresh(dish)

        return dish

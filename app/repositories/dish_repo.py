from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Dish
from app.repositories import BaseRepo


class DishRepo(BaseRepo):
    def __init__(self, db: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(model=Dish, db=db)

    async def get_all(self, **kwargs) -> list:
        dishes = await self.db.execute(
            select(Dish).where(Dish.submenu_id == kwargs['submenu_id'])
        )

        return list(dishes.scalars())

    async def create(self, **kwargs) -> Dish:
        price = round(float(kwargs['dish_in'].price), 2)
        kwargs['dish_in'].price = str(price)

        dish = Dish(**kwargs['dish_in'].model_dump(), submenu_id=kwargs['submenu_id'])

        self.db.add(dish)
        await self.db.commit()
        await self.db.refresh(dish)

        return dish

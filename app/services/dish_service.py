from uuid import UUID

from fastapi.responses import JSONResponse
from ..schemas.dish_schemas import DishAdd, DishUpdate, DishResponse
from ..repositories import DishRepo
from fastapi import Depends


class DishService:
    def __init__(self, dish_repo: DishRepo = Depends()):
        self._dish_repo = dish_repo

    async def get_one_dish(self, id: UUID):
        dish = await self._dish_repo.get_one(id)

        if not dish:
            return JSONResponse(
                status_code=404,
                content={"detail": "dish not found"},
            )

        return dish

    async def get_all_dishes(self):
        return await self._dish_repo.get_all()

    async def create_dish(self, dish_in: DishAdd, submenu_id: UUID):
        
        dish = await self._dish_repo.create(dish_in, submenu_id)
        return dish

    async def delete_dish(self, id: UUID):
        return await self._dish_repo.delete(id)

    async def update_dish(self, dish_upd: DishUpdate, id: UUID):
        dish_upd = await self._dish_repo.update(dish_upd, id)

        if dish_upd.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"detail": "dish not found"},
            )

        dish = await self._dish_repo.get_one(id)
        return dish

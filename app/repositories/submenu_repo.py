from uuid import UUID
from fastapi import Depends
from app.repositories import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import distinct, func, select
from sqlalchemy.orm import aliased

from ..schemas.submenu_schemas import SubmenuAdd

from ..core.db import get_async_session
from ..models import Submenu, Dish


class SubmenuRepo(BaseRepo):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db
        super().__init__(model=Submenu, db=self.db)

    async def get_one(self, id: UUID):
        try:
            submenu = aliased(Submenu)
            dish = aliased(Dish)

            query = (
                select(
                    submenu.id,
                    submenu.title,
                    submenu.description,
                    func.count(distinct(dish.id)).label("dishes_count"),
                )
                .outerjoin(dish, submenu.id == dish.submenu_id)
                .where(submenu.id == id)
                .group_by(submenu.id)
            )

            submenu = await self.db.execute(query)

            return submenu.first()
        except Exception as error:
            return error

    async def get_all(self):
        submenu = aliased(Submenu)
        dish = aliased(Dish)

        query = (
            select(
                submenu.id,
                submenu.title,
                submenu.description,
                func.count(distinct(dish.id)).label("dishes_count"),
            )
            .outerjoin(dish, submenu.id == dish.submenu_id)
            .group_by(submenu.id)
        )

        result = await self.db.execute(query)
        submenus = result.fetchall()

        return submenus

    async def create(self, submenu_in: SubmenuAdd, menus_id: UUID):
        obj = Submenu(**submenu_in.model_dump(), menu_id=menus_id)

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)

        return obj

from uuid import UUID

from fastapi import Depends
from sqlalchemy import Row, Sequence, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.repositories import BaseRepo

from ..core.db import get_async_session
from ..models import Dish, Submenu


class SubmenuRepo(BaseRepo):
    def __init__(self, db: AsyncSession = Depends(get_async_session)) -> None:
        self.db = db
        super().__init__(model=Submenu, db=self.db)

    async def get_one(self, id: UUID) -> Row[tuple[UUID, str, int]]:
        try:
            submenu = aliased(Submenu)
            dish = aliased(Dish)

            query = (
                select(
                    submenu.id,
                    submenu.title,
                    submenu.description,
                    func.count(distinct(dish.id)).label('dishes_count'),
                )
                .outerjoin(dish, submenu.id == dish.submenu_id)
                .where(submenu.id == id)
                .group_by(submenu.id)
            )

            submenu = await self.db.execute(query)

            return submenu.first()
        except Exception as error:
            return error

    async def get_all(self, **kwargs) -> Sequence[Row[tuple[UUID, str, int]]]:
        submenu = aliased(Submenu)
        dish = aliased(Dish)

        query = (
            select(
                submenu.id,
                submenu.title,
                submenu.description,
                func.count(distinct(dish.id)).label('dishes_count'),
            )
            .outerjoin(dish, submenu.id == dish.submenu_id)
            .group_by(submenu.id)
            .where(submenu.menu_id == kwargs['menu_id'])
        )

        result = await self.db.execute(query)
        submenus = result.fetchall()

        return submenus

    async def create(self, **kwargs) -> Submenu:
        obj = Submenu(**kwargs['submenu_in'].model_dump(), menu_id=kwargs['menus_id'])

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)

        return obj

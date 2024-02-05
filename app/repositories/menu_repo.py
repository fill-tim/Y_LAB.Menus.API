from uuid import UUID

from fastapi import Depends
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.core.db import get_async_session
from app.models import Dish, Menu, Submenu
from app.repositories import BaseRepo


class MenuRepo(BaseRepo):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.db = db
        super().__init__(model=Menu, db=self.db)

    async def get_one(self, id: UUID):
        menu = aliased(Menu)
        submenu = aliased(Submenu)
        dish = aliased(Dish)

        query = (
            select(
                menu.id,
                menu.title,
                menu.description,
                func.count(distinct(submenu.id)).label('submenu_count'),
                func.count(distinct(dish.id)).label('dishes_count'),
            )
            .outerjoin(
                submenu,
                menu.id == submenu.menu_id,
            )
            .outerjoin(dish, submenu.id == dish.submenu_id)
            .where(menu.id == id)
            .group_by(menu.id)
        )

        menu = await self.db.execute(query)

        return menu.first()

    async def get_all(self):
        menu = aliased(Menu)
        submenu = aliased(Submenu)
        dish = aliased(Dish)

        query = (
            select(
                menu.id,
                menu.title,
                menu.description,
                func.count(distinct(submenu.id)).label('submenu_count'),
                func.count(distinct(dish.id)).label('dishes_count'),
            )
            .outerjoin(
                submenu,
                menu.id == submenu.menu_id,
            )
            .outerjoin(dish, submenu.id == dish.submenu_id)
            .group_by(menu.id)
        )

        result = await self.db.execute(query)
        menus = result.fetchall()

        return menus

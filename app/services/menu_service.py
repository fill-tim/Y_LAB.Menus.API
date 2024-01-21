from uuid import UUID

from fastapi.responses import JSONResponse
from ..schemas.menu_schemas import MenuAdd, MenuUpdate
from ..repositories import MenuRepo
from fastapi import Depends


class MenuService:
    def __init__(self, menu_repo: MenuRepo = Depends()):
        self._menu_repo = menu_repo

    async def get_one_menu(self, id: UUID):
        menu = await self._menu_repo.get_one(id)

        if not menu:
            return JSONResponse(
                status_code=404,
                content={"detail": "menu not found"},
            )

        return {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": menu.submenu_count,
            "dishes_count": menu.dishes_count,
        }

    async def get_all_menus(self):
        menus = await self._menu_repo.get_all()
        response = []

        for menu in menus:
            response.append(
                {
                    "id": menu.id,
                    "title": menu.title,
                    "description": menu.description,
                    "submenus_count": menu.submenu_count,
                    "dishes_count": menu.dishes_count,
                }
            )
        return response

    async def create_menu(self, menu_in: MenuAdd):
        return await self._menu_repo.create(menu_in)

    async def delete_menu(self, id: UUID):
        return await self._menu_repo.delete(id)

    async def update_menu(self, menu_upd: MenuUpdate, id: UUID):
        menu_upd = await self._menu_repo.update(menu_upd, id)

        if menu_upd.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"detail": "menu not found"},
            )

        menu = await self._menu_repo.get_one(id)

        return {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": menu.submenu_count,
            "dishes_count": menu.dishes_count,
        }

from uuid import UUID

from fastapi.responses import JSONResponse
from ..schemas.submenu_schemas import SubmenuAdd, SubmenuUpdate
from ..repositories import SubmenuRepo
from fastapi import Depends


class SubmenuService:
    def __init__(self, submenu_repo: SubmenuRepo = Depends()):
        self._submenu_repo = submenu_repo

    async def get_one_submenu(self, id: UUID):
        submenu = await self._submenu_repo.get_one(id)

        if not submenu:
            return JSONResponse(
                status_code=404,
                content={"detail": "submenu not found"},
            )

        return {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": submenu.dishes_count,
        }

    async def get_all_submenus(self):
        submenus = await self._submenu_repo.get_all()

        response = []

        for submenu in submenus:
            response.append(
                {
                    "id": submenu.id,
                    "title": submenu.title,
                    "description": submenu.description,
                    "dishes_count": submenu.dishes_count,
                }
            )

        return response

    async def create_submenu(self, submenu_in: SubmenuAdd, menus_id: UUID):
        return await self._submenu_repo.create(submenu_in, menus_id)

    async def delete_submenu(self, id: UUID):
        return await self._submenu_repo.delete(id)

    async def update_submenu(self, sub_menu_upd: SubmenuUpdate, id: UUID):
        submenu_upd = await self._submenu_repo.update(sub_menu_upd, id)

        if submenu_upd.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"detail": "submenu not found"},
            )

        submenu = await self._submenu_repo.get_one(id)

        return {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": submenu.dishes_count,
        }

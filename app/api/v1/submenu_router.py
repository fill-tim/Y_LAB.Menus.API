from uuid import UUID
from fastapi import APIRouter
from ...services.submenu_service import SubmenuService
from fastapi import Depends
from ...schemas.submenu_schemas import (
    SubmenuResponse,
    SubmenuAdd,
    SubmenuUpdate,
    CreatedSubmenu,
    UpdatedSubmenu,
)


submenu_router = APIRouter(prefix="/api/v1/menus/{menus_id}", tags=["submenus"])


@submenu_router.get("/submenus")
async def list(
    menus_id: UUID,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.get_all_submenus(menus_id)


@submenu_router.get("/submenus/{id}", response_model=SubmenuResponse)
async def get(id: UUID, submenu_service: SubmenuService = Depends()):
    return await submenu_service.get_one_submenu(id)


@submenu_router.post("/submenus", status_code=201, response_model=CreatedSubmenu)
async def create(
    menus_id: UUID, submenu_in: SubmenuAdd, submenu_service: SubmenuService = Depends()
):
    return await submenu_service.create_submenu(submenu_in, menus_id)


@submenu_router.delete("/submenus/{id}")
async def delete(id: UUID, menus_id: UUID, submenu_service: SubmenuService = Depends()):
    return await submenu_service.delete_submenu(id)


@submenu_router.patch("/submenus/{id}", response_model=UpdatedSubmenu)
async def update(
    id: UUID,
    submenu_upd: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.update_submenu(submenu_upd, id)

from uuid import UUID
from fastapi import APIRouter
from ...services.menu_service import MenuService
from fastapi import Depends
from ...schemas.menu_schemas import (
    MenuResponse,
    MenuAdd,
    MenuUpdate,
    CreatedMenu,
    UpdatedMenu,
)

menu_router = APIRouter(prefix="/api/v1", tags=["menus"])


@menu_router.get("/menus")
async def list(
    menu_service: MenuService = Depends(),
):
    return await menu_service.get_all_menus()


@menu_router.get("/menus/{id}", response_model=MenuResponse)
async def get(id: UUID, menu_service: MenuService = Depends()):
    return await menu_service.get_one_menu(id)


@menu_router.post("/menus", status_code=201, response_model=CreatedMenu)
async def create(menu_in: MenuAdd, menu_service: MenuService = Depends()):
    return await menu_service.create_menu(menu_in)


@menu_router.delete("/menus/{id}")
async def delete(id: UUID, menu_service: MenuService = Depends()):
    return await menu_service.delete_menu(id)


@menu_router.patch("/menus/{id}", response_model=UpdatedMenu)
async def update(id: UUID, menu_upd: MenuUpdate, menu_service: MenuService = Depends()):
    return await menu_service.update_menu(menu_upd, id)

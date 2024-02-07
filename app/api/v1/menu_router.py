from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ...schemas.menu_schemas import (
    CreatedMenu,
    DeletedMenu,
    MenuAdd,
    MenuErrors,
    MenuResponse,
    MenuUpdate,
    UpdatedMenu,
)
from ...services.menu_service import MenuService

menu_router = APIRouter(
    prefix='/api/v1',
    tags=['menus'],
    responses={400: {'model': MenuErrors}},
)


@menu_router.get('/menus', response_model=list[MenuResponse])
async def list_menu(
    menu_service: MenuService = Depends(),
) -> list[MenuResponse] | JSONResponse:
    return await menu_service.get_all_menus()


@menu_router.get(
    '/menus/{menu_id}',
    response_model=MenuResponse,
    responses={404: {'model': MenuErrors}},
)
async def get_menu(
    menu_id: UUID, menu_service: MenuService = Depends()
) -> MenuResponse | JSONResponse:
    return await menu_service.get_one_menu(menu_id=menu_id)


@menu_router.post('/menus', status_code=201, response_model=CreatedMenu)
async def create_menu(
    menu_in: MenuAdd, menu_service: MenuService = Depends()
) -> CreatedMenu | JSONResponse:
    return await menu_service.create_menu(menu_in=menu_in)


@menu_router.delete('/menus/{menu_id}', response_model=DeletedMenu)
async def delete_menu(
    menu_id: UUID, menu_service: MenuService = Depends()
) -> DeletedMenu | JSONResponse:
    return await menu_service.delete_menu(menu_id=menu_id)


@menu_router.patch('/menus/{menu_id}', response_model=UpdatedMenu)
async def update_menu(
    menu_id: UUID, menu_upd: MenuUpdate, menu_service: MenuService = Depends()
) -> UpdatedMenu | JSONResponse:
    return await menu_service.update_menu(menu_upd=menu_upd, menu_id=menu_id)

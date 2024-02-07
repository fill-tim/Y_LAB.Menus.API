from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ...schemas.submenu_schemas import (
    CreatedSubmenu,
    DeletedSubmenu,
    SubmenuAdd,
    SubmenuErrors,
    SubmenuResponse,
    SubmenuUpdate,
    UpdatedSubmenu,
)
from ...services.submenu_service import SubmenuService

submenu_router = APIRouter(
    prefix='/api/v1/menus/{menu_id}',
    tags=['submenus'],
    responses={400: {'model': SubmenuErrors}},
)


@submenu_router.get('/submenus', response_model=list[SubmenuResponse])
async def list_submenu(
    menu_id: UUID, submenu_service: SubmenuService = Depends()
) -> list[SubmenuResponse] | JSONResponse:
    return await submenu_service.get_all_submenus(menu_id=menu_id)


@submenu_router.get(
    '/submenus/{submenu_id}',
    response_model=SubmenuResponse,
    responses={404: {'model': SubmenuErrors}},
)
async def get_submenu(
    submenu_id: UUID, menu_id: UUID, submenu_service: SubmenuService = Depends()
) -> SubmenuResponse | JSONResponse:
    return await submenu_service.get_one_submenu(submenu_id=submenu_id)


@submenu_router.post('/submenus', status_code=201, response_model=CreatedSubmenu)
async def create_submenu(
    menu_id: UUID, submenu_in: SubmenuAdd, submenu_service: SubmenuService = Depends()
) -> CreatedSubmenu | JSONResponse:
    return await submenu_service.create_submenu(submenu_in=submenu_in, menu_id=menu_id)


@submenu_router.delete('/submenus/{submenu_id}', response_model=DeletedSubmenu)
async def delete_submenu(
    submenu_id: UUID,
    menu_id: UUID,
    submenu_service: SubmenuService = Depends(),
) -> DeletedSubmenu | JSONResponse:
    return await submenu_service.delete_submenu(submenu_id=submenu_id, menu_id=menu_id)


@submenu_router.patch('/submenus/{submenu_id}', response_model=UpdatedSubmenu)
async def update_submenu(
    submenu_id: UUID,
    menu_id: UUID,
    submenu_upd: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(),
) -> UpdatedSubmenu | JSONResponse:
    return await submenu_service.update_submenu(
        submenu_upd=submenu_upd, submenu_id=submenu_id, menu_id=menu_id
    )

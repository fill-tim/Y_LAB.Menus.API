from uuid import UUID

from fastapi import APIRouter, Depends

from ...schemas.submenu_schemas import (
    CreatedSubmenu,
    DeletedSubmenu,
    SubmenuAdd,
    SubmenuResponse,
    SubmenuUpdate,
    UpdatedSubmenu,
)
from ...services.submenu_service import SubmenuService

submenu_router = APIRouter(prefix='/api/v1/menus/{menu_id}', tags=['submenus'])


@submenu_router.get('/submenus', response_model=list[SubmenuResponse])
async def list(
    menu_id: UUID,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.get_all_submenus(menu_id=menu_id)


@submenu_router.get('/submenus/{id}', response_model=SubmenuResponse)
async def get(id: UUID, menu_id: UUID, submenu_service: SubmenuService = Depends()):
    return await submenu_service.get_one_submenu(id=id)


@submenu_router.post('/submenus', status_code=201, response_model=CreatedSubmenu)
async def create(
    menu_id: UUID, submenu_in: SubmenuAdd, submenu_service: SubmenuService = Depends()
):
    return await submenu_service.create_submenu(submenu_in=submenu_in, menu_id=menu_id)


@submenu_router.delete('/submenus/{id}', response_model=DeletedSubmenu)
async def delete(
    id: UUID,
    menu_id: UUID,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.delete_submenu(id=id, menu_id=menu_id)


@submenu_router.patch('/submenus/{id}', response_model=UpdatedSubmenu)
async def update(
    id: UUID,
    menu_id: UUID,
    submenu_upd: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.update_submenu(
        submenu_upd=submenu_upd, id=id, menu_id=menu_id
    )

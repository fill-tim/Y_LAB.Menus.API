from uuid import UUID

from fastapi import APIRouter, Depends

from ...schemas.dish_schemas import (
    CreatedDish,
    DeletedDish,
    DishAdd,
    DishResponse,
    DishUpdate,
    UpdatedDish,
)
from ...services.dish_service import DishService

dish_router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['dishes']
)


@dish_router.get('/dishes', response_model=list[DishResponse])
async def list(
    menu_id: UUID,
    submenu_id: UUID,
    dish_service: DishService = Depends(),
):
    return await dish_service.get_all_dishes(submenu_id=submenu_id, menu_id=menu_id)


@dish_router.get('/dishes/{id}', response_model=DishResponse)
async def get(id: UUID, dish_service: DishService = Depends()):
    return await dish_service.get_one_dish(id=id)


@dish_router.post('/dishes', status_code=201, response_model=CreatedDish)
async def create(
    submenu_id: UUID,
    menu_id: UUID,
    dish_in: DishAdd,
    dish_service: DishService = Depends(),
):
    return await dish_service.create_dish(
        dish_in=dish_in, submenu_id=submenu_id, menu_id=menu_id
    )


@dish_router.delete('/dishes/{id}', response_model=DeletedDish)
async def delete(
    id: UUID, menu_id: UUID, submenu_id: UUID, dish_service: DishService = Depends()
):
    return await dish_service.delete_dish(id=id, menu_id=menu_id, submenu_id=submenu_id)


@dish_router.patch('/dishes/{id}', response_model=UpdatedDish)
async def update(
    id: UUID,
    submenu_id: UUID,
    menu_id: UUID,
    dish_upd: DishUpdate,
    dish_service: DishService = Depends(),
):
    return await dish_service.update_dish(
        dish_upd=dish_upd, id=id, submenu_id=submenu_id
    )

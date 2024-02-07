from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ...schemas.dish_schemas import (
    CreatedDish,
    DeletedDish,
    DishAdd,
    DishErrors,
    DishResponse,
    DishUpdate,
    UpdatedDish,
)
from ...services.dish_service import DishService

dish_router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    tags=['dishes'],
    responses={400: {'model': DishErrors}},
)


@dish_router.get('/dishes', response_model=list[DishResponse])
async def list_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_service: DishService = Depends(),
) -> list[DishResponse] | JSONResponse:
    return await dish_service.get_all_dishes(submenu_id=submenu_id, menu_id=menu_id)


@dish_router.get(
    '/dishes/{dish_id}',
    response_model=DishResponse,
    responses={404: {'model': DishErrors}},
)
async def get_dish(
    dish_id: UUID, dish_service: DishService = Depends()
) -> DishResponse | JSONResponse:
    return await dish_service.get_one_dish(dish_id=dish_id)


@dish_router.post('/dishes', status_code=201, response_model=CreatedDish)
async def create_dish(
    submenu_id: UUID,
    menu_id: UUID,
    dish_in: DishAdd,
    dish_service: DishService = Depends(),
) -> CreatedDish | JSONResponse:
    return await dish_service.create_dish(
        dish_in=dish_in, submenu_id=submenu_id, menu_id=menu_id
    )


@dish_router.delete('/dishes/{dish_id}', response_model=DeletedDish)
async def delete_dish(
    dish_id: UUID,
    menu_id: UUID,
    submenu_id: UUID,
    dish_service: DishService = Depends(),
) -> DeletedDish | JSONResponse:
    return await dish_service.delete_dish(
        dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id
    )


@dish_router.patch('/dishes/{dish_id}', response_model=UpdatedDish)
async def update_dish(
    dish_id: UUID,
    submenu_id: UUID,
    menu_id: UUID,
    dish_upd: DishUpdate,
    dish_service: DishService = Depends(),
) -> UpdatedDish | JSONResponse:
    return await dish_service.update_dish(
        dish_upd=dish_upd, dish_id=dish_id, submenu_id=submenu_id
    )

from uuid import UUID
from fastapi import APIRouter
from ...services.dish_service import DishService
from fastapi import Depends
from ...schemas.dish_schemas import (
    DishResponse,
    DishAdd,
    DishUpdate,
    UpdatedDish,
    CreatedDish,
)


dish_router = APIRouter(
    prefix="/api/v1/menus/{menus_id}/submenus/{submenu_id}", tags=["dishes"]
)


@dish_router.get("/dishes")
async def list(
    dish_service: DishService = Depends(),
):
    return await dish_service.get_all_dishes()


@dish_router.get("/dishes/{id}", response_model=DishResponse)
async def get(id: UUID, dish_service: DishService = Depends()):
    return await dish_service.get_one_dish(id)


@dish_router.post("/dishes", status_code=201, response_model=CreatedDish)
async def create(
    submenu_id: UUID,
    dish_in: DishAdd,
    dish_service: DishService = Depends(),
):
    return await dish_service.create_dish(dish_in, submenu_id)


@dish_router.delete("/dishes/{id}")
async def delete(id: UUID, dish_service: DishService = Depends()):
    return await dish_service.delete_dish(id)


@dish_router.patch("/dishes/{id}", response_model=UpdatedDish)
async def update(
    id: UUID,
    dish_upd: DishUpdate,
    dish_service: DishService = Depends(),
):
    return await dish_service.update_dish(dish_upd, id)

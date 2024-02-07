from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from ..repositories import DishRepo
from ..schemas.dish_schemas import Dish, DishAdd, DishUpdate
from .helpers.redis_cache import RedisCache


class DishService:
    def __init__(
        self, dish_repo: DishRepo = Depends(), redis_cache: RedisCache = Depends()
    ) -> None:
        self._dish_repo = dish_repo
        self._redis_cache = redis_cache

    async def get_one_dish(self, dish_id: UUID) -> dict | JSONResponse:
        try:
            cache: bytes = await self._redis_cache.get_value(str(dish_id))

            if cache:
                return await self._redis_cache.convert_to_json(cache)
            else:
                dish: any = await self._dish_repo.get_one(dish_id)

                if not dish:
                    return JSONResponse(
                        status_code=404,
                        content={'detail': 'dish not found'},
                    )

                response: dict = {
                    'id': dish.id,
                    'title': dish.title,
                    'description': dish.description,
                    'price': dish.price,
                }

                await self._redis_cache.set_value(
                    key=str(dish_id),
                    value=str(response),
                    tags=[str(dish_id)],
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def get_all_dishes(
        self, submenu_id: UUID, menu_id: UUID
    ) -> list[dict] | JSONResponse:
        try:
            cache: bytes = await self._redis_cache.get_value(f'submenu/{submenu_id}')

            if cache is not None:
                return await self._redis_cache.convert_to_json(cache)
            else:
                dishes: list = await self._dish_repo.get_all(submenu_id=submenu_id)

                response: list = []

                for dish in dishes:
                    response.append(
                        {
                            'id': str(dish.id),
                            'title': dish.title,
                            'description': dish.description,
                            'price': dish.price,
                        }
                    )

                await self._redis_cache.set_value(
                    key=f'submenu/{submenu_id}',
                    value=str(response),
                    tags=[f'submenu/{submenu_id}', f'menu/{menu_id}'],
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def create_dish(
        self, dish_in: DishAdd, submenu_id: UUID, menu_id: UUID
    ) -> dict | JSONResponse:
        try:
            dish: Dish = await self._dish_repo.create(
                dish_in=dish_in, submenu_id=submenu_id
            )

            await self._redis_cache.del_cache(
                tags=[
                    'Menus',
                    f'menu/{menu_id}',
                    f'submenu/{submenu_id}',
                    str(menu_id),
                    str(submenu_id),
                ]
            )

            return dish
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def delete_dish(
        self, dish_id: UUID, submenu_id: UUID, menu_id: UUID
    ) -> dict[str, bool] | JSONResponse:
        try:
            response: any = await self._dish_repo.delete(dish_id)

            if response.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'dish not found'},
                )

            await self._redis_cache.del_cache(
                tags=[
                    'Menus',
                    f'menu/{menu_id}',
                    f'submenu/{submenu_id}',
                    str(dish_id),
                    str(menu_id),
                    str(submenu_id),
                ],
            )

            return {'status': True, 'message': 'The dish has been deleted'}
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def update_dish(
        self, dish_upd: DishUpdate, dish_id: UUID, submenu_id: UUID
    ) -> dict | JSONResponse:
        try:
            upd_dish: any = await self._dish_repo.update(dish_upd, dish_id)

            if upd_dish.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'dish not found'},
                )

            dish: any = await self._dish_repo.get_one(dish_id)

            await self._redis_cache.del_cache(
                tags=[f'submenu/{submenu_id}', str(dish_id)],
            )

            return dish
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

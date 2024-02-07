from typing import Any
from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import Row

from ..repositories import SubmenuRepo
from ..schemas.submenu_schemas import Submenu, SubmenuAdd, SubmenuUpdate
from .helpers.redis_cache import RedisCache


class SubmenuService:
    def __init__(
        self, submenu_repo: SubmenuRepo = Depends(), redis_cache: RedisCache = Depends()
    ) -> None:
        self._submenu_repo = submenu_repo
        self._redis_cache = redis_cache

    async def get_one_submenu(
        self,
        submenu_id: UUID,
    ) -> dict[str, int] | JSONResponse:
        try:

            cache: bytes | None = await self._redis_cache.get_value(str(submenu_id))

            if cache is not None:
                return await self._redis_cache.convert_to_json(cache)
            else:
                submenu: Row = await self._submenu_repo.get_one(submenu_id)

                if not submenu:
                    return JSONResponse(
                        status_code=404,
                        content={'detail': 'submenu not found'},
                    )

                response: dict = {
                    'id': submenu.id,
                    'title': submenu.title,
                    'description': submenu.description,
                    'dishes_count': submenu.dishes_count,
                }

                await self._redis_cache.set_value(
                    key=str(submenu_id),
                    value=str(response),
                    tags=[str(submenu_id)],
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def get_all_submenus(
        self, menu_id: UUID
    ) -> list[dict[str, int]] | JSONResponse:
        try:
            cache: bytes | None = await self._redis_cache.get_value(
                f'get_all_submenus{menu_id}'
            )

            if cache:
                return await self._redis_cache.convert_to_json(cache)
            else:
                submenus: Row = await self._submenu_repo.get_all(menu_id=menu_id)

                response: list = []

                for submenu in submenus:
                    response.append(
                        {
                            'id': str(submenu.id),
                            'title': submenu.title,
                            'description': submenu.description,
                            'dishes_count': submenu.dishes_count,
                        }
                    )

                await self._redis_cache.set_value(
                    key=f'get_all_submenus{menu_id}',
                    value=str(response),
                    tags=[
                        f'menu/{menu_id}',
                    ],
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def create_submenu(
        self, submenu_in: SubmenuAdd, menu_id: UUID
    ) -> dict | JSONResponse:
        try:
            submenu: Submenu = await self._submenu_repo.create(
                submenu_in=submenu_in, menus_id=menu_id
            )

            await self._redis_cache.del_cache(
                tags=['Menus', str(menu_id), f'menu/{menu_id}']
            )

            return submenu
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def delete_submenu(
        self, submenu_id: UUID, menu_id: UUID
    ) -> dict[str, bool] | JSONResponse:
        try:
            response: Any = await self._submenu_repo.delete(submenu_id)

            if response.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'submenu not found'},
                )

            await self._redis_cache.del_cache(
                tags=[
                    'Menus',
                    f'menu/{menu_id}',
                    str(id),
                    str(menu_id),
                ],
            )

            return {'status': True, 'message': 'The submenu has been deleted'}
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def update_submenu(
        self, submenu_upd: SubmenuUpdate, submenu_id: UUID, menu_id: UUID
    ) -> dict[str, int] | JSONResponse:
        try:
            upd_submenu: Any = await self._submenu_repo.update(submenu_upd, submenu_id)

            if upd_submenu.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'submenu not found'},
                )

            submenu: Row = await self._submenu_repo.get_one(submenu_id)

            await self._redis_cache.del_cache(tags=[f'menu/{menu_id}', str(submenu_id)])

            return {
                'id': submenu.id,
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': submenu.dishes_count,
            }
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

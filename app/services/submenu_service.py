from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from ..repositories import SubmenuRepo
from ..schemas.submenu_schemas import SubmenuAdd, SubmenuUpdate
from .helpers.redis_cache import RedisCache


class SubmenuService:
    def __init__(
        self, submenu_repo: SubmenuRepo = Depends(), redis_cache: RedisCache = Depends()
    ):
        self._submenu_repo = submenu_repo
        self._redis_cache = redis_cache

    async def get_one_submenu(
        self,
        id: UUID,
    ):
        try:

            cache = await self._redis_cache.get_value(str(id))

            if cache is not None:
                return await self._redis_cache.convert_to_json(cache)
            else:
                submenu = await self._submenu_repo.get_one(id)

                if not submenu:
                    return JSONResponse(
                        status_code=404,
                        content={'detail': 'submenu not found'},
                    )

                response = {
                    'id': submenu.id,
                    'title': submenu.title,
                    'description': submenu.description,
                    'dishes_count': submenu.dishes_count,
                }

                await self._redis_cache.set_value(
                    key=str(id),
                    value=str(response),
                    tags=[str(id)],
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def get_all_submenus(self, menu_id: UUID):
        try:
            cache = await self._redis_cache.get_value(f'get_all_submenus{menu_id}')

            if cache:
                return await self._redis_cache.convert_to_json(cache)
            else:
                submenus = await self._submenu_repo.get_all(menu_id)

                response = []

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

    async def create_submenu(self, submenu_in: SubmenuAdd, menu_id: UUID):
        try:
            submenu = await self._submenu_repo.create(
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

    async def delete_submenu(self, id: UUID, menu_id: UUID):
        try:
            response = await self._submenu_repo.delete(id)

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

    async def update_submenu(self, submenu_upd: SubmenuUpdate, id: UUID, menu_id: UUID):
        try:
            submenu_upd = await self._submenu_repo.update(submenu_upd, id)

            if submenu_upd.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'submenu not found'},
                )

            submenu = await self._submenu_repo.get_one(id)

            await self._redis_cache.del_cache(tags=[f'menu/{menu_id}', str(id)])

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

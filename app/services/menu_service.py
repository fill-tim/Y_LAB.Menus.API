from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from ..repositories import MenuRepo
from ..schemas.menu_schemas import MenuAdd, MenuUpdate
from .helpers.redis_cache import RedisCache


class MenuService:
    def __init__(
        self, menu_repo: MenuRepo = Depends(), redis_cache: RedisCache = Depends()
    ):
        self._menu_repo = menu_repo
        self._redis_cache = redis_cache

    async def get_one_menu(self, id: UUID):
        try:
            cache = await self._redis_cache.get_value(str(id))

            if cache is not None:
                res = await self._redis_cache.convert_to_json(cache)
                return res
            else:
                menu = await self._menu_repo.get_one(id)

                if not menu:
                    return JSONResponse(
                        status_code=404,
                        content={'detail': 'menu not found'},
                    )

                response = {
                    'id': str(menu.id),
                    'title': menu.title,
                    'description': menu.description,
                    'submenus_count': menu.submenu_count,
                    'dishes_count': menu.dishes_count,
                }

                await self._redis_cache.set_value(
                    key=str(id), value=str(response), tags=[str(id)]
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def get_all_menus(self):
        try:
            cache = await self._redis_cache.get_value('Menus')

            if cache:
                return await self._redis_cache.convert_to_json(cache)
            else:
                menus = await self._menu_repo.get_all()

                response = []

                for menu in menus:
                    response.append(
                        {
                            'id': str(menu.id),
                            'title': menu.title,
                            'description': menu.description,
                            'submenus_count': menu.submenu_count,
                            'dishes_count': menu.dishes_count,
                        }
                    )

                await self._redis_cache.set_value(
                    key='get_all_menus',
                    value=str(response),
                    tags=['Menus'],
                )

                return response
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def create_menu(self, menu_in: MenuAdd):
        try:
            menu = await self._menu_repo.create(obj_in=menu_in)

            await self._redis_cache.del_cache(['Menus'])

            return menu
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def delete_menu(self, id: UUID) -> dict:
        try:
            response = await self._menu_repo.delete(id)

            if response.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'menu not found'},
                )

            await self._redis_cache.del_cache(
                tags=['Menus', f'menu/{id}', str(id)],
            )

            return {'status': True, 'message': 'The menu has been deleted'}
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

    async def update_menu(self, menu_upd: MenuUpdate, id: UUID) -> dict:
        try:
            menu_upd = await self._menu_repo.update(menu_upd, id)

            if menu_upd.rowcount == 0:
                return JSONResponse(
                    status_code=404,
                    content={'detail': 'menu not found'},
                )

            menu = await self._menu_repo.get_one(id)

            await self._redis_cache.del_cache(tags=['Menus', str(id)])

            return {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
                'submenus_count': menu.submenu_count,
                'dishes_count': menu.dishes_count,
            }
        except Exception as error:
            return JSONResponse(
                status_code=400,
                content={'detail': f'{error}'},
            )

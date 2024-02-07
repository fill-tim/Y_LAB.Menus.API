from typing import Any
from uuid import UUID

from sqlalchemy import delete, select, update


class BaseRepo:
    def __init__(self, model, db) -> None:
        self.model = model
        self.db = db

    async def get_one(self, id: UUID) -> Any | Exception:
        try:
            obj = await self.db.execute(select(self.model).filter_by(id=id))

            return obj.scalar()
        except Exception as error:
            return error

    async def get_all(self) -> list | Any:
        try:
            objs = await self.db.execute(select(self.model))
            return list(objs.scalars())
        except Exception as error:
            return error

    async def create(self, **kwargs) -> Any | Exception:
        try:
            obj = self.model(**kwargs['obj_in'].model_dump())

            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)

            return obj
        except Exception as error:
            return error

    async def update(self, obj_upd, id: UUID) -> Any | Exception:
        try:
            updated_obj = await self.db.execute(
                update(self.model)
                .filter_by(id=id)
                .values(obj_upd.model_dump(exclude_unset=True))
            )
            await self.db.commit()

            return updated_obj
        except Exception as error:
            return error

    async def delete(self, id: UUID) -> Any | Exception:
        try:
            deleted_obj = await self.db.execute(delete(self.model).filter_by(id=id))
            await self.db.commit()

            return deleted_obj
        except Exception as error:
            return error

from uuid import UUID

from fastapi import Body
from pydantic import BaseModel


class Submenu(BaseModel):
    title: str
    description: str


class SubmenuAdd(Submenu):
    pass


class SubmenuUpdate(BaseModel):
    title: str | None = Body(None)
    description: str | None = Body(None)


class DeletedSubmenu(BaseModel):
    status: bool
    message: str


class SubmenuResponse(Submenu):
    id: UUID
    dishes_count: int


class CreatedSubmenu(Submenu):
    id: UUID


class UpdatedSubmenu(SubmenuResponse):
    pass

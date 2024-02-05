from uuid import UUID

from fastapi import Body
from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str


class MenuAdd(Menu):
    pass


class CreatedMenu(Menu):
    id: UUID


class DeletedMenu(BaseModel):
    status: bool
    message: str


class MenuUpdate(BaseModel):
    title: str | None = Body(None)
    description: str | None = Body(None)


class MenuResponse(Menu):
    id: UUID
    submenus_count: int
    dishes_count: int


class UpdatedMenu(MenuResponse):
    pass

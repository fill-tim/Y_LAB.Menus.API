from uuid import UUID
from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str


class MenuAdd(Menu):
    pass


class CreatedMenu(Menu):
    id: UUID


class UpdatedMenu(CreatedMenu):
    pass


class MenuUpdate(Menu):
    pass


class MenuResponse(Menu):
    id: UUID
    submenus_count: int
    dishes_count: int

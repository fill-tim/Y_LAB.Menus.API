from uuid import UUID
from pydantic import BaseModel


class Submenu(BaseModel):
    title: str
    description: str


class SubmenuAdd(Submenu):
    pass


class SubmenuUpdate(Submenu):
    pass


class SubmenuResponse(Submenu):
    id: UUID
    dishes_count: int


class CreatedSubmenu(Submenu):
    id: UUID


class UpdatedSubmenu(Submenu):
    id: UUID

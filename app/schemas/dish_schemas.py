from uuid import UUID

from fastapi import Body
from pydantic import BaseModel


class Dish(BaseModel):
    title: str
    description: str
    price: str | float


class DishAdd(Dish):
    pass


class DishUpdate(BaseModel):
    title: str | None = Body(None)
    description: str | None = Body(None)
    price: str | float | None = Body(None)


class DeletedDish(BaseModel):
    status: bool
    message: str


class DishResponse(Dish):
    id: UUID


class CreatedDish(Dish):
    id: UUID


class UpdatedDish(DishUpdate):
    id: UUID

from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel


class Dish(BaseModel):
    title: str
    description: str
    price: Union[str, float]


class DishAdd(Dish):
    pass


class DishUpdate(Dish):
    pass


class DishResponse(Dish):
    id: UUID


class CreatedDish(Dish):
    id: UUID


class UpdatedDish(Dish):
    id: UUID

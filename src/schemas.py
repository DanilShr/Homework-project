from datetime import date
from typing import Optional

from pydantic import BaseModel


class Recipes(BaseModel):
    name: str
    time_dish: int
    ingredients: str
    description: Optional[str]


class RecipesOut(Recipes):

    class Config:
        orm_mode = True

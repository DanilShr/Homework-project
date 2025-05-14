from typing import List, Optional

from fastapi import FastAPI
from sqlalchemy import update
from sqlalchemy.future import select

import schemas
from database import Base, engine, session
from models import Recipes as RecipeModel

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/recipes", response_model=
List[schemas.RecipesOut])
@app.get("/recipes/{idx}", response_model=List[schemas.RecipesOut])
async def get_recipe(idx: Optional[int] = None) -> List[schemas.RecipesOut]:
    if idx:
        result = await session.execute(
            select(
                RecipeModel.name,
                RecipeModel.time_dish,
                RecipeModel.ingredients,
                RecipeModel.description,
            )
            .where(RecipeModel.id == idx)
            .order_by(RecipeModel.count, RecipeModel.time_dish)
        )

        query = (
            update(RecipeModel)
            .where(RecipeModel.id == idx)
            .values(count=RecipeModel.count + 1)
        )
        await session.execute(query)
        recipe_data = result.mappings().all()
        print(recipe_data)
        if recipe_data:
            recipe_data = [schemas.RecipesOut(**recipe) for recipe in recipe_data]
            return recipe_data
    else:
        result = await session.execute(
            select(
                RecipeModel.name,
                RecipeModel.time_dish,
                RecipeModel.ingredients,
                RecipeModel.description,
            ).order_by(RecipeModel.count, RecipeModel.time_dish)
        )
        recipe_data = result.mappings().all()
        print(recipe_data)
        if recipe_data:
            recipe_data = [schemas.RecipesOut(**recipe) for recipe in recipe_data]
        return recipe_data


@app.post("/recipes", response_model=schemas.Recipes)
async def create_recipe(recipes: schemas.Recipes) -> RecipeModel:
    new_recipes = RecipeModel(**recipes.dict())
    async with session.begin():
        session.add(new_recipes)
    return new_recipes

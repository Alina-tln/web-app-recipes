import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from database import async_session
import recipe_service.models.recipes as recipes
import recipe_service.models.ingredients as ingredients
from translation_service.models.translations import RecipeTranslation
import recipe_service.pydantic_schemas.recipes as RecipesSchema
import recipe_service.pydantic_schemas.ingredients as IngredientsSchema
from db_create_tables import setup_database

app = FastAPI()

async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

#Lounch creating tables
setup_database()

@app.post("/ingredient_category", summary="Add ingredient category", tags=["Ingredients"])
async def add_category(category: IngredientsSchema, session: SessionDep):
    new_category = ingredients.Category(
        name=category.name
    )
    session.add(new_category)
    await session.commit()
    return {"Result": True}

if __name__ == "__main__":
    uvicorn.run("main.app", reload=True)













# 1. Standard library imports
import logging
from typing import Annotated

# 2. Third-party imports
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 3. Local application imports
from database import async_session
from recipe_service.services.category_service import CategoryService
from recipe_service.services.ingredient_service import IngredientService
from recipe_service.services.recipe_service import RecipeService

# ----------------------------------------------------------
# Setting up logging
# ----------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("recipe_service")


# ----------------------------------------------------------
# Session Dependency
# ----------------------------------------------------------
async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ----------------------------------------------------------
# Service Dependencies
# ----------------------------------------------------------
# Category Service
def get_category_service(session: SessionDep) -> CategoryService:
    """A dependency that provides an instance of CategoryService."""
    return CategoryService(session)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]


# Ingredient Service
def get_ingredient_service(session: SessionDep) -> IngredientService:
    """A dependency that provides an instance of IngredientService."""
    return IngredientService(session)


IngredientServiceDep = Annotated[CategoryService, Depends(get_ingredient_service)]


# Recipe Service
def get_recipe_service(session: SessionDep) -> RecipeService:
    """A dependency that provides an instance of RecipeService."""
    return RecipeService(session)


RecipeServiceDep = Annotated[CategoryService, Depends(get_ingredient_service)]

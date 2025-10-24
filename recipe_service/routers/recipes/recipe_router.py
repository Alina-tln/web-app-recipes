# 1. Standard library imports
from typing import List
from functools import wraps

# 2. Third-party imports
from fastapi import HTTPException, status, APIRouter

# 3. Local application imports
import recipe_service.pydantic_schemas.recipes_schemas as schemas
from recipe_service.examples.recipe_examples import recipe_examples

from recipe_service.services.recipe_service import (
    RecipeAlreadyExists,
    RecipeNotFound,
    IngredientNotFound
)

from recipe_service.core.dependencies import (RecipeServiceDep, logger)


# ----------------------------------------------------------
# Router
# ----------------------------------------------------------
router = APIRouter(
    prefix="/recipes",
)


# ----------------------------------------------------------
# Decorator for handling RecipeNotFound
# ----------------------------------------------------------
def handle_not_found(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RecipeNotFound as e:
            raise HTTPException(status_code=404, detail="Recipe not found") from e
        except IngredientNotFound as e:
            raise HTTPException(status_code=404, detail=f"Ingredients not found: {e}") from e
    return wrapper


# ----------------------------------------------------------
# CRUD Endpoints
# ----------------------------------------------------------
# CREATE
@router.post(
    "",
    summary="Add new recipe",
    response_model=schemas.RecipeReadSchema,
    openapi_extra=recipe_examples["create"]
)
async def add_recipe(
        recipe: schemas.RecipeCreateSchema,
        service: RecipeServiceDep
):
    try:
        new_recipe = await service.create_recipe(recipe)
        logger.info(f"Created recipe ID={new_recipe.id} with ingredients "
                    f"{[i.ingredient_id for i in recipe.ingredients]}")
        return new_recipe
    except RecipeAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


# READ ALL
@router.get("",
            summary="Get all recipes",
            response_model=List[schemas.RecipeReadSchema],
            openapi_extra=recipe_examples["get_all"])
async def get_recipes(service: RecipeServiceDep):
    recipes = await service.get_all_recipes()
    logger.info(f"Retrieved all recipes, count={len(recipes)}")
    return recipes


# READ ONE
@router.get(
    "/{recipe_id}",
    summary="Get recipe by ID",
    response_model=schemas.RecipeReadSchema,
    openapi_extra=recipe_examples["get_one"])
@handle_not_found
async def get_recipe_by_id(
        recipe_id: int,
        service: RecipeServiceDep
):
    recipe = await service.get_recipe_by_id(recipe_id)
    logger.info(f"Retrieved recipe ID={recipe.id}")
    return recipe


# UPDATE
@router.put("/{recipe_id}",
            summary="Update recipe",
            response_model=schemas.RecipeReadSchema,
            openapi_extra=recipe_examples["update"])
@handle_not_found
async def update_recipe_by_id(
        recipe_id: int,
        updated: schemas.RecipeUpdateSchema,
        service: RecipeServiceDep
):
    try:
        updated_recipe = await service.update_recipe(recipe_id, updated)
        logger.info(f"Updated recipe ID={updated_recipe.id}")
        return updated_recipe
    except RecipeAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


# DELETE
@router.delete(
    "/{recipe_id}",
    summary="Delete recipe",
    response_model=schemas.DeleteResponseSchema)
@handle_not_found
async def delete_recipe(recipe_id: int, service: RecipeServiceDep):
    deleted_name = await service.delete_recipe(recipe_id)
    logger.info(f"Deleted recipe ID={recipe_id}, name={deleted_name!r}")
    return {"Result": True, "id": recipe_id, "name": deleted_name}

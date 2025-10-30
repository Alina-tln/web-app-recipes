from functools import wraps

from fastapi import APIRouter, HTTPException, Query
from typing import List

from pydantic.v1 import Field

from recipe_service.pydantic_schemas.recipes_schemas import (
    RecipeCreateSchema, RecipeUpdateSchema, RecipeReadSchema, DeleteResponseSchema
)
from recipe_service.services.recipe_service import RecipeNotFound, IngredientNotFound
from recipe_service.core.dependencies import RecipeServiceDep
from recipe_service.examples.recipe_examples import recipe_examples

router = APIRouter(prefix="/recipes")


def handle_not_found(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RecipeNotFound as e:
            raise HTTPException(status_code=404, detail="Recipe not found") from e
        except IngredientNotFound as e:
            raise HTTPException(
                status_code=404,
                detail=f"Ingredients not found: {e}"
            ) from e
    return wrapper


@router.post(
    "",
    response_model=RecipeReadSchema,
    openapi_extra=recipe_examples["create"])
async def add_recipe(
        recipe: RecipeCreateSchema,
        service: RecipeServiceDep):
    try:
        return await service.create_recipe(recipe)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get(
    "",
    response_model=List[RecipeReadSchema],
    openapi_extra=recipe_examples["get_all"]
)
async def get_recipes(service: RecipeServiceDep):
    return await service.get_all_recipes()


@router.get(
    "/search",
    response_model=List[RecipeReadSchema],
    openapi_extra=recipe_examples["search"]
)
@handle_not_found
async def search_recipes(
        service: RecipeServiceDep,
        ingredient_ids: List[int] =  Query(
            ...,
            description="IDs of ingredients to search for",
            example=[1, 3]),
        match_all: bool = Query(
            default=False,
            description="If true, recipe must contain all ingredients",
            example=False)
):
    match_mode = "all" if match_all else "any"
    recipes = await service.search_recipes(ingredient_ids, match_mode)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found with given ingredients")
    return recipes


@router.get(
    "/{recipe_id}",
    response_model=RecipeReadSchema,
    openapi_extra=recipe_examples["get_one"])
@handle_not_found
async def get_recipe(recipe_id: int, service: RecipeServiceDep):
    return await service.get_recipe_by_id(recipe_id)


@router.put(
    "/{recipe_id}",
    response_model=RecipeReadSchema,
    openapi_extra=recipe_examples["update"]
)
@handle_not_found
async def update_recipe(
        recipe_id: int,
        updated: RecipeUpdateSchema,
        service: RecipeServiceDep):
    return await service.update_recipe(recipe_id, updated)


@router.delete(
    "/{recipe_id}",
    response_model=DeleteResponseSchema,
    openapi_extra=recipe_examples["delete"]
)
@handle_not_found
async def delete_recipe(recipe_id: int, service: RecipeServiceDep):
    deleted_id = await service.delete_recipe(recipe_id)
    return {"Result": True, "id": deleted_id}

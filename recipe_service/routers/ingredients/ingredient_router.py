#1. Standard library imports
from typing import List
from functools import wraps

# 2. Third-party imports
from fastapi import HTTPException, status, APIRouter

# 3. Local application imports
import recipe_service.pydantic_schemas.ingredients_schemas as schemas
from recipe_service.examples.ingredient_examples import ingredient_examples

from recipe_service.services.ingredient_service import (
    IngredientAlreadyExists,
    IngredientNotFound
)

from recipe_service.core.dependencies import (IngredientServiceDep, logger)

# ----------------------------------------------------------
# Router
# ----------------------------------------------------------
router = APIRouter(
    prefix="/ingredients",
)

# ----------------------------------------------------------
# Decorator for handling IngredientNotFound
# ----------------------------------------------------------
def handle_not_found(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IngredientNotFound:
            raise HTTPException(status_code=404, detail="Ingredient not found")
    return wrapper

# ----------------------------------------------------------
# CRUD Endpoints
# ----------------------------------------------------------
# CREATE
@router.post(
    "",
    summary="Add new ingredient",
    response_model=schemas.IngredientReadSchema,
    openapi_extra=ingredient_examples["create"]
)
async def add_ingredient(
        ingredient: schemas.IngredientCreateSchema,
        service: IngredientServiceDep
):
    try:
        # All database logic has been moved to service.ingredient_service
        new_ingredient = await service.create_ingredient(ingredient.name, ingredient.categories)
        logger.info(f"Added ingredient: {new_ingredient.name} (id={new_ingredient.id}, category={new_ingredient.categories})")
        return new_ingredient

    except IngredientAlreadyExists as e:
        # Convert a custom exception to HTTP 409 Conflict
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

# READ ALL
@router.get("",
            summary="Get all ingredients",
            response_model=List[schemas.IngredientReadSchema],
            openapi_extra=ingredient_examples["get_all"])
async def get_ingredients(service: IngredientServiceDep):
    ingredients = await service.get_all_ingredients()
    logger.info(f"Retrieved all ingredients, count={len(ingredients)}")
    # service returns a Sequence, FastAPI/Pydantic converts it to a List
    return ingredients

# READ ONE
@router.get(
    "/{ingredient_id}",
    summary="Get ingredient by ID",
    response_model=schemas.IngredientReadSchema,
    openapi_extra=ingredient_examples["get_one"])
@handle_not_found
async def get_ingredient_by_id(
        ingredient_id: int,
        service: IngredientServiceDep
):
    ingredient = await service.get_ingredient_by_id(ingredient_id)
    logger.info(f"Retrieved ingredient ID={ingredient.id}")
    return ingredient

# UPDATE
@router.put("/{ingredient_id}",
            summary="Update ingredient",
            response_model=schemas.IngredientReadSchema,
            openapi_extra=ingredient_examples["update"]
            )
@handle_not_found
async def update_ingredient_by_id(
        ingredient_id: int,
        updated: schemas.IngredientUpdateSchema,
        service: IngredientServiceDep
):
    try:
        updated_ingredient = await service.update_ingredient_by_id(ingredient_id, updated.name)
        logger.info(f"Updated ingredient ID={updated_ingredient.id} -> {updated_ingredient.name}")
        return updated_ingredient

    except IngredientAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


# DELETE
@router.delete(
    "/{ingredient_id}",
    summary="Delete ingredient",
    response_model=schemas.DeleteResponseSchema)
@handle_not_found
async def delete_ingredient(ingredient_id: int, service: IngredientServiceDep):
    deleted = await service.delete_ingredient(ingredient_id)
    logger.info(f"Deleted ingredient ID={ingredient_id}, name='{deleted}'")
    return {"Result": True, "id": ingredient_id, "name": deleted}

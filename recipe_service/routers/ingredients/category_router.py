#1. Standard library imports
from typing import List
from functools import wraps

# 2. Third-party imports
from fastapi import HTTPException, status, APIRouter

# 3. Local application imports
import recipe_service.pydantic_schemas.ingredients_schemas as schemas
from recipe_service.examples.category_examples import category_examples

from recipe_service.services.category_service import (
    CategoryAlreadyExists,
    CategoryNotFound
)

from recipe_service.core.dependencies import (CategoryServiceDep, logger)

# ----------------------------------------------------------
# Router
# ----------------------------------------------------------
router = APIRouter(
    prefix="/ingredient_category",
)

# ----------------------------------------------------------
# Decorator for handling CategoryNotFound
# ----------------------------------------------------------
def handle_not_found(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CategoryNotFound:
            raise HTTPException(status_code=404, detail="Category not found")
    return wrapper

# ----------------------------------------------------------
# CRUD Endpoints
# ----------------------------------------------------------
# CREATE
@router.post(
    "",
    summary="Add new ingredient category",
    response_model=schemas.CategoryReadSchema,
    openapi_extra=category_examples["create"]
)
async def add_category(
        category: schemas.CategoryCreateSchema,
        service: CategoryServiceDep
):
    try:
        # All database logic has been moved to service.category_service.create_category
        new_category = await service.create_category(category.name)
        logger.info(f"Added category: {new_category.name} (id={new_category.id})")
        return new_category

    except CategoryAlreadyExists as e:
        # Convert a custom exception to HTTP 409 Conflict
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

# READ ALL
@router.get("",
         summary="Get all ingredient categories",
         response_model=List[schemas.CategoryReadSchema],
         openapi_extra=category_examples["get_all"])
async def get_categories(service: CategoryServiceDep):
    categories = await service.get_all_categories()
    logger.info(f"Retrieved all categories, count={len(categories)}")
    # service returns a Sequence, FastAPI/Pydantic converts it to a List
    return categories

# READ ONE
@router.get(
    "/{category_id}",
    summary="Get ingredient category by ID",
    response_model=schemas.CategoryReadSchema,
    openapi_extra=category_examples["get_one"])
@handle_not_found
async def get_category_by_id(
        category_id: int,
        service: CategoryServiceDep
):
    category = await service.get_category_by_id(category_id)
    logger.info(f"Retrieved category ID={category.id}")
    return category

# UPDATE
@router.put("/{category_id}",
         summary="Update ingredient category",
         response_model=schemas.CategoryReadSchema,
         openapi_extra=category_examples["update"]
         )
@handle_not_found
async def update_category_by_id(
        category_id: int,
        updated: schemas.CategoryUpdateSchema,
        service: CategoryServiceDep
):
    try:
        updated_category = await service.update_category(category_id, updated.name)
        logger.info(f"Updated category ID={updated_category.id} -> {updated_category.name}")
        return updated_category

    except CategoryAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


# DELETE
@router.delete(
    "/{category_id}",
    summary="Delete ingredient category",
    response_model=schemas.DeleteResponseSchema)
@handle_not_found
async def delete_category(category_id: int, service: CategoryServiceDep):
    deleted_name = await service.delete_category(category_id)
    logger.info(f"Deleted category ID={category_id}, name='{deleted_name}'")
    return {"Result": True, "id": category_id, "name": deleted_name}

# 1. Standard library imports
import logging
from typing import Annotated, List

# 2. Third-party imports
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

# 3. Local application imports
from database import async_session
import recipe_service.pydantic_schemas.ingredients as schemas
from recipe_service.examples import category_examples

from recipe_service.services.category_service import (
    CategoryService,
    CategoryAlreadyExists,
    CategoryNotFound
)


# ----------------------------------------------------------
# Setting up logging
# ----------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("recipe_service")

# ----------------------------------------------------------
# Initializing the Application
# ----------------------------------------------------------
app = FastAPI(
    title="Recipe Service API",
    description="API for managing recipes and ingredients",
    version="1.0.0"
)

# ----------------------------------------------------------
# Session Dependency
# ----------------------------------------------------------
async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_category_service(session: SessionDep) -> CategoryService:
    """A dependency that provides an instance of CategoryService."""
    return CategoryService(session)

CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]

# ----------------------------------------------------------
# SQLAlchemy Global Error Interception Middleware
# ----------------------------------------------------------
@app.middleware("http")
async def db_error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal database error"}
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


# ----------------------------------------------------------
# Endpoint for adding an ingredient category
# ----------------------------------------------------------
# CREATE
@app.post(
    "/ingredient_category",
    summary="Add new ingredient category",
    tags=["Categories"],
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
        return {"Result": True, "id": new_category.id, "name": new_category.name}

    except CategoryAlreadyExists as e:
        # Convert a custom exception to HTTP 409 Conflict
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

# READ ALL
@app.get("/ingredient_category",
         summary="Get all ingredient categories",
         response_model=List[schemas.CategoryReadSchema],
         tags=["Categories"],
         openapi_extra=category_examples["get_all"])
async def get_categories(service: CategoryServiceDep):
    categories = await service.get_all_categories()
    # service returns a Sequence, FastAPI/Pydantic converts it to a List
    return categories

# READ ONE
@app.get(
    "/ingredient_category/{category_id}",
    summary="Get ingredient category by ID",
    tags=["Categories"],
    openapi_extra=category_examples["get_one"])
async def get_category(category_id: int, service: CategoryServiceDep):
    category = await service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# UPDATE
@app.put("/ingredient_category/{category_id}",
         summary="Update ingredient category",
         tags=["Categories"],
         openapi_extra=category_examples["update"]
         )

async def update_category(
        category_id: int,
        updated: schemas.CategoryUpdateSchema,
        service: CategoryServiceDep
):
    try:
        updated_category = await service.update_category(category_id, updated.name)

        logger.info(f"Updated category ID={updated_category.id} -> {updated_category.name}")
        return {"id": updated_category.id, "name": updated_category.name}

    except CategoryNotFound:
        # Convert a custom exception to HTTP 404 Not Found
        raise HTTPException(status_code=404, detail="Category not found")


# DELETE
@app.delete(
    "/ingredient_category/{category_id}",
    summary="Delete ingredient category",
    tags=["Categories"])
async def delete_category(category_id: int, service: CategoryServiceDep):
    try:
        deleted_name = await service.delete_category(category_id)

        logger.info(f"Deleted category ID={category_id}")
        return {"Result": True, "message": f"Category '{deleted_name}' deleted."}

    except CategoryNotFound:
        # Convert a custom exception to HTTP 404 Not Found
        raise HTTPException(status_code=404, detail="Category not found")

# ----------------------------------------------------------
# Entrypoint
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("recipe_service.main:app", reload=True)
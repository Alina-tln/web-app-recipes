# 1. Standard library imports
import logging
from typing import Annotated, Any, AsyncGenerator

# 2. Third-party imports
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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
async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        try:
            yield session
            logger.debug("Session successfully yielded")
        except IntegrityError as e:
            # Roll back a transaction if constraints (unique, foreign key, etc.) are violated.
            await session.rollback()
            logger.warning(f"Integrity error: {e.orig}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e.orig}"
            )
        except SQLAlchemyError as e:
            # Any other SQLAlchemy errors (problems with transaction, query, etc.)
            await session.rollback()
            logger.error(f"Database error: {type(e).__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal database error"
            )
        except Exception as e:
            # Unknown errors (we log and forward them further)
            await session.rollback()
            logger.exception(f"Unexpected error during DB operation: {e}")
            raise
        finally:
            await session.close()
            logger.debug("Session closed")

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


RecipeServiceDep = Annotated[CategoryService, Depends(get_recipe_service)]

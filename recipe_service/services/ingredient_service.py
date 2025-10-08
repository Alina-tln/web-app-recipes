from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Type

from sqlalchemy.orm import InstrumentedAttribute

from recipe_service.models import ingredients_models as models
import logging

# ----------------------------------------------------------
# Custom exceptions
# ----------------------------------------------------------
class IngredientAlreadyExists(Exception):
    """An exception is thrown when a ingredient with the same name already exists."""
    def __init__(self, name: str):
        super().__init__(f"Ingredient '{name}' already exists.")

class IngredientNotFound(Exception):
    """Exception thrown when ingredient by ID is not found."""
    def __init__(self, category_id: int):
        super().__init__(f"Ingredient with ID {category_id} not found.")


# ----------------------------------------------------------
# Category service
# ----------------------------------------------------------
class IngredientService:
    """Service class for managing ingredient."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.Ingredient = models.Ingredient

    async def create_ingredient(self, name: str, category_ids: list[int]) -> models.Ingredient:
        """Creates a new ingredient, checking for duplicates."""
        if not category_ids:
            raise ValueError("Ingredient must belong to at least one category")

        result = await self.session.execute(
            select(self.Ingredient).where(self.Ingredient.name == name)
        )
        if result.scalar_one_or_none():
            raise IngredientAlreadyExists(name=name)

        categories = (await self.session.scalars(select(models.Category).where(models.Category.id.in_(category_ids)))).all()
        if len(categories) != len(category_ids):
            raise ValueError("Some categories not found")

        new_ingredient = self.Ingredient(name=name, categories=categories)
        self.session.add(new_ingredient)
        await self.session.commit()
        await self.session.refresh(new_ingredient)

        return new_ingredient

    async def get_all_ingredients(self) -> Sequence[models.Ingredient]:
        """Return all ingredients"""
        result = await self.session.execute(select(self.Ingredient).order_by(self.Ingredient.id))
        return result.scalars().all()

    async def get_ingredient_by_id(self, ingredient_id: int) -> Type[models.Ingredient]:
        """Return ingredient by id"""
        ingredient = await self.session.get(self.Ingredient, ingredient_id)
        if ingredient is None:
            raise IngredientNotFound(ingredient_id)
        return ingredient

    async def update_ingredient(self, ingredient_id: int, new_name: str = None, category_ids: list[int] = None) -> Type[models.Ingredient]:
        """Updates an ingredient by id"""
        ingredient = await self.get_ingredient_by_id(ingredient_id)
        if not ingredient:
            raise IngredientNotFound(ingredient_id)

        if ingredient.name == new_name:
            logging.info(f"No change in ingredient name (id={ingredient_id}, name={new_name})")
            return ingredient

        if category_ids is not None:
            categories = (await self.session.scalars(select(models.Category).where(models.Category.id.in_(category_ids)))).all()
            if not categories:
                raise ValueError("Ingredient must have at least one valid category")
            ingredient.categories = categories

        existing = await self.session.execute(
            select(self.Ingredient).where(self.Ingredient.name == new_name)
        )
        if existing.scalar_one_or_none():
            raise IngredientAlreadyExists(new_name)

        ingredient.name = new_name
        try:
            await self.session.commit()
            await self.session.refresh(ingredient)
            return ingredient
        except IntegrityError:
            await self.session.rollback()
            raise IngredientAlreadyExists(new_name)

    async def delete_ingredient(self, ingredient_id: int) -> InstrumentedAttribute:
        """Deletes a ingredient by id"""
        ingredient = await self.get_ingredient_by_id(ingredient_id)
        if not ingredient:
            raise IngredientNotFound(ingredient_id)

        deleted = ingredient.name
        await self.session.delete(ingredient)
        await self.session.commit()

        return deleted

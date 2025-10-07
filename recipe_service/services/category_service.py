"""
Custom exceptions
"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Sequence
from recipe_service.models import ingredients as models
import logging

class CategoryAlreadyExists(Exception):
    """An exception is thrown when a category with the same name already exists."""
    def __init__(self, name: str):
        super().__init__(f"Category '{name}' already exists.")

class CategoryNotFound(Exception):
    """Exception thrown when category by ID is not found."""
    def __init__(self, category_id: int):
        super().__init__(f"Category with ID {category_id} not found.")


class CategoryService:
    """Service class for managing ingredient categories."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.Category = models.Category

    async def create_category(self, name: str) -> models.Category:
        """Creates a new category, checking for duplicates."""

        # Check for existence
        result = await self.session.execute(
            select(self.Category).where(self.Category.name == name)
        )
        if result.scalar_one_or_none():
            raise CategoryAlreadyExists(name=name)

        # Creation and saving
        new_category = self.Category(name=name)
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)

        return new_category

    async def get_all_categories(self) -> Sequence[models.Category]:
        """Return all categories"""
        result = await self.session.execute(select(self.Category).order_by(self.Category.id))
        return result.scalars().all()

    async def get_category_by_id(self, category_id: int) -> Optional[models.Category]:
        """Return category by id"""
        return await self.session.get(self.Category, category_id)

    async def update_category(self, category_id: int, new_name: str) -> models.Category:
        """Updates a category by id"""
        category = await self.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFound(category_id)

        if category.name == new_name:
            logging.info(f"No change in category name (id={category_id}, name={new_name})")
            return category

        existing = await self.session.execute(
            select(self.Category).where(self.Category.name == new_name)
        )
        if existing.scalar_one_or_none():
            raise CategoryAlreadyExists(new_name)

        category.name = new_name
        try:
            await self.session.commit()
            await self.session.refresh(category)
            return category
        except IntegrityError:
            await self.session.rollback()
            raise CategoryAlreadyExists(new_name)

    async def delete_category(self, category_id: int) -> str:
        """Deletes a category by id"""
        category = await self.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFound(category_id)

        deleted_name = category.name
        await self.session.delete(category)
        await self.session.commit()

        return deleted_name

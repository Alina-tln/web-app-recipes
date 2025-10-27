from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from recipe_service.models.recipes_models import Recipe, RecipeIngredient
from recipe_service.models.ingredients_models import Ingredient
from recipe_service.pydantic_schemas.recipes_schemas import (
    RecipeCreateSchema,
    RecipeUpdateSchema
)




class RecipeAlreadyExists(Exception):
    pass




class RecipeNotFound(Exception):
    pass




class IngredientNotFound(Exception):
    pass


class RecipeService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def _validate_ingredients(self, ingredient_ids: list[int]):
        result = await self.session.scalars(
            select(Ingredient).where(Ingredient.id.in_(ingredient_ids))
        )
        ingredients = result.all()
        missing = set(ingredient_ids) - {i.id for i in ingredients}
        if missing:
            raise IngredientNotFound(list(missing))


    async def create_recipe(self, data: RecipeCreateSchema, author_id: int | None = None):
        await self._validate_ingredients([i.ingredient_id for i in data.ingredients])
        recipe = Recipe(
            cooking_time_in_minutes=data.cooking_time_in_minutes,
            image_url=data.image_url,
            author_id=author_id,
        )
        self.session.add(recipe)
        await self.session.flush()
        self.session.add_all([
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=i.ingredient_id,
                quantity=i.quantity,
                unit_id=i.unit_id
            )
            for i in data.ingredients
        ])
        await self.session.commit()
        await self.session.refresh(recipe)
        result = await self.session.execute(
            select(Recipe)
            .options(
                selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient)
            )
            .where(Recipe.id == recipe.id)
        )
        recipe = result.scalar_one()
        return recipe


    async def get_all_recipes(self):
        result = await self.session.execute(
            select(Recipe).options(selectinload(Recipe.ingredients))
        )
        return result.scalars().all()


    async def get_recipe_by_id(self, recipe_id: int):
        result = await self.session.execute(
            select(Recipe)
            .options(selectinload(Recipe.ingredients))
            .where(Recipe.id == recipe_id)
        )
        recipe = result.scalar_one_or_none()
        if not recipe:
            raise RecipeNotFound
        return recipe


    async def update_recipe(self, recipe_id: int, data: RecipeUpdateSchema):
        recipe = await self.get_recipe_by_id(recipe_id)
        updated = False


        if data.cooking_time_in_minutes is not None:
            recipe.cooking_time_in_minutes = data.cooking_time_in_minutes
            updated = True
        if data.image_url is not None:
            recipe.image_url = data.image_url
            updated = True
        if data.ingredients is not None:
            await self._validate_ingredients([i.ingredient_id for i in data.ingredients])
            await self.session.execute(
                delete(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)
            )
            self.session.add_all([
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=i.ingredient_id,
                    quantity=i.quantity,
                    unit_id=i.unit_id
                )
                for i in data.ingredients
            ])
            updated = True


        if updated:
            await self.session.commit()
            await self.session.refresh(recipe)
        return recipe


    async def delete_recipe(self, recipe_id: int):
        recipe = await self.get_recipe_by_id(recipe_id)
        await self.session.delete(recipe)
        await self.session.commit()
        return recipe.id

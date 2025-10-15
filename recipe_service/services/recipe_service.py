import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import selectinload

from recipe_service.models.recipes_models import Recipe, RecipeIngredient
from recipe_service.models.ingredients_models import Ingredient
from recipe_service.pydantic_schemas.recipes_schemas import (
    RecipeCreateSchema,
    RecipeUpdateSchema
)

# ----------------------------------------------------------
# Logger configuration
# ----------------------------------------------------------
logger = logging.getLogger("recipe_service")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# ----------------------------------------------------------
# Custom exceptions
# ----------------------------------------------------------
class RecipeAlreadyExists(Exception):
    pass


class RecipeNotFound(Exception):
    pass


class IngredientNotFound(Exception):
    pass


# ----------------------------------------------------------
# Recipe service
# ----------------------------------------------------------
class RecipeService:
    """Service class for managing admin recipes."""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.Recipe = Recipe
        self.RecipeIngredient = RecipeIngredient
        self.Ingredient = Ingredient

    # ------------------ Private methods ------------------
    async def _validate_ingredients(self, ingredient_ids: list[int]):
        result = await self.session.scalars(
            select(self.Ingredient)
            .where(self.Ingredient.id.in_(ingredient_ids)
                   )
        )
        ingredients = result.all()
        missing = set(ingredient_ids) - {i.id for i in ingredients}
        if missing:
            logger.warning(f"Missing ingredients: {missing}")
            raise IngredientNotFound(list(missing))

    async def _check_duplicate(
            self,
            author_id: int | None,
            image_url: str | None,
            exclude_id: int | None = None):
        if not author_id or not image_url:
            return
        query = (select(self.Recipe)
                 .where(and_(self.Recipe.author_id == author_id,
                             self.Recipe.image_url == image_url)
                        )
                 )
        if exclude_id:
            query = query.where(self.Recipe.id != exclude_id)
        if await self.session.scalar(query):
            logger.warning(
                (
                    f"Duplicate recipe detected for author_id={author_id} "
                    f"and image_url={image_url}"
                )
            )
            raise RecipeAlreadyExists

    async def _sync_ingredients(self, recipe: Recipe, new_ingredients: list) -> bool:
        """Synchronize recipe ingredients with new data. Returns True if any changes."""
        updated = False
        current_dict = {ri.ingredient_id: ri for ri in recipe.ingredients}
        new_dict = {i.ingredient_id: i for i in new_ingredients}

        # Delete removed
        to_delete = set(current_dict.keys()) - set(new_dict.keys())
        if to_delete:
            logger.info(f"Recipe {recipe.id}: deleting ingredients {to_delete}")
            await self.session.execute(
                delete(self.RecipeIngredient).where(
                    self.RecipeIngredient.recipe_id == recipe.id,
                    self.RecipeIngredient.ingredient_id.in_(to_delete)
                )
            )
            updated = True

        # Update existing
        for ing_id, new_ing in new_dict.items():
            if ing_id in current_dict:
                cur = current_dict[ing_id]
                if cur.quantity != new_ing.quantity or cur.unit_id != new_ing.unit_id:
                    logger.info(
                        f"Recipe {recipe.id}: updating ingredient {ing_id} "
                        f"(quantity {cur.quantity}->{new_ing.quantity}, "
                        f"unit_id {cur.unit_id}->{new_ing.unit_id})"
                    )
                    cur.quantity = new_ing.quantity
                    cur.unit_id = new_ing.unit_id
                    updated = True

        # Insert new
        inserts = [i for i in new_ingredients if i.ingredient_id not in current_dict]
        if inserts:
            logger.info(
                (f"Recipe {recipe.id}: adding new ingredients "
                 f"{[i.ingredient_id for i in inserts]}"
                 )
            )
            self.session.add_all([
                self.RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=i.ingredient_id,
                    quantity=i.quantity,
                    unit_id=i.unit_id
                )
                for i in inserts
            ])
            updated = True

        return updated

    # ------------------ CREATE ------------------
    async def create_recipe(self, data: RecipeCreateSchema) -> Recipe:
        if not data.ingredients:
            raise ValueError("Recipe must have at least one ingredient.")

        ingredient_ids = [i.ingredient_id for i in data.ingredients]
        await self._validate_ingredients(ingredient_ids)
        await self._check_duplicate(data.author_id, data.image_url)

        async with self.session.begin():
            recipe = self.Recipe(
                author_id=data.author_id,
                cooking_time_in_minutes=data.cooking_time_in_minutes,
                image_url=data.image_url
            )
            self.session.add(recipe)
            await self.session.flush()
            self.session.add_all([
                self.RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=i.ingredient_id,
                    quantity=i.quantity,
                    unit_id=i.unit_id
                )
                for i in data.ingredients
            ])
        logger.info(f"Created recipe id={recipe.id} with ingredients {ingredient_ids}")
        return recipe

    # ------------------ READ ------------------
    async def get_all_recipes(self) -> list[Recipe]:
        result = await self.session.execute(
            select(self.Recipe)
            .options(selectinload(self.Recipe.ingredients)
                     )
        )
        recipes = result.scalars().all()
        logger.info(f"Retrieved {len(recipes)} recipes")
        return recipes

    async def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        result = await self.session.execute(
            select(self.Recipe)
            .options(selectinload(self.Recipe.ingredients))
            .where(self.Recipe.id == recipe_id)
        )
        recipe = result.scalar_one_or_none()
        if not recipe:
            logger.warning(f"Recipe {recipe_id} not found")
            raise RecipeNotFound
        return recipe

    # ------------------ UPDATE ------------------
    async def update_recipe(self, recipe_id: int, data: RecipeUpdateSchema) -> Recipe:
        recipe = await self.get_recipe_by_id(recipe_id)
        updated = False

        # Base fields
        if (data.cooking_time_in_minutes is not None
                and recipe.cooking_time_in_minutes != data.cooking_time_in_minutes):
            logger.info(
                (
                    f"Recipe {recipe_id}: cooking_time_in_minutes "
                    f"{recipe.cooking_time_in_minutes}->{data.cooking_time_in_minutes}"
                )
            )
            recipe.cooking_time_in_minutes = data.cooking_time_in_minutes
            updated = True

        if data.image_url is not None and recipe.image_url != data.image_url:
            await self._check_duplicate(
                recipe.author_id,
                data.image_url,
                exclude_id=recipe_id
            )
            logger.info(
                (f"Recipe {recipe_id}: image_url {recipe.image_url}->{data.image_url}")
            )
            recipe.image_url = data.image_url
            updated = True

        if data.ingredients is not None:
            await self._validate_ingredients(
                [
                    i.ingredient_id for i in data.ingredients
                ]
            )
            if await self._sync_ingredients(recipe, data.ingredients):
                updated = True

        if updated:
            async with self.session.begin():
                self.session.add(recipe)
            logger.info(f"Recipe {recipe_id} updated")
        else:
            logger.info(f"No changes detected for recipe {recipe_id}")

        return recipe

    # ------------------ DELETE ------------------
    async def delete_recipe(self, recipe_id: int) -> int:
        recipe = await self.get_recipe_by_id(recipe_id)
        async with self.session.begin():
            await self.session.delete(recipe)
        logger.info(f"Deleted recipe {recipe_id}")
        return recipe.id

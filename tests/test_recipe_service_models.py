import pytest
from recipe_service.models.recipes_models import (
    Recipe,
    UserRecipeIngredient,
    UserRecipe,
    Unit,
    RecipeIngredient
)
from recipe_service.models.ingredients_models import Category, Ingredient


@pytest.fixture
def sample_data(session):
    # Creating base objects
    category = Category(name="Vegetables")
    ingredient = Ingredient(name="Tomato")
    unit = Unit(symbol="g")
    ingredient.categories.append(category)

    session.add_all([category, ingredient, unit])
    session.flush()

    # Recipe
    recipe = Recipe(author_id=1, cooking_time_in_minutes=15)
    session.add(recipe)
    session.flush()

    # RecipeIngredient
    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient.id,
        quantity=100,
        unit_id=unit.id
    )
    session.add(recipe_ingredient)

    # UserRecipe
    user_recipe = UserRecipe(
        base_recipe_id=recipe.id,
        user_id=1,
        title="My Tomato Salad",
        description="Custom description",
        instructions="Cut and serve"
    )
    session.add(user_recipe)
    session.flush()

    # UserRecipeIngredient
    user_recipe_ingredient = UserRecipeIngredient(
        user_recipe_id=user_recipe.id,
        ingredient_id=ingredient.id,
        unit_id=unit.id,
        quantity=100
    )
    session.add(user_recipe_ingredient)

    session.commit()

    return {
        "ingredient": ingredient,
        "category": category,
        "unit": unit,
        "recipe": recipe,
        "user_recipe": user_recipe
    }


def test_recipe_author_and_ingredients(sample_data):
    recipe = sample_data["recipe"]
    ingredient = sample_data["ingredient"]

    assert recipe.author_id == 1
    assert ingredient in [ri.ingredient for ri in recipe.ingredients]
    assert recipe in [ri.recipe for ri in ingredient.recipe_ingredients]


def test_category_ingredient(sample_data):
    ingredient = sample_data["ingredient"]
    category = sample_data["category"]

    assert category in ingredient.categories
    assert ingredient in category.ingredients


def test_user_recipe_and_links(sample_data):
    user_recipe = sample_data["user_recipe"]
    recipe = sample_data["recipe"]

    assert user_recipe.base_recipe == recipe
    assert user_recipe.user_id == 1
    assert any(ing.ingredient.name == "Tomato" for ing in user_recipe.ingredients)

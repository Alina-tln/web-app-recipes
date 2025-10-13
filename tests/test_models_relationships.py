import pytest
from recipe_service.models.recipes_models import (
    Recipe,
    UserRecipeIngredient,
    UserRecipe,
    Unit,
    RecipeIngredient
)
from recipe_service.models.ingredients_models import Category, Ingredient
from translation_service.models.translations import (
    UnitTranslation,
    RecipeTranslation,
    IngredientTranslation,
    Language
)
from user_service.models.users import User
from user_service.models.groups import UserGroup, Group


@pytest.fixture
def sample_data(session):
    # Creating base objects
    user = User(username="alex", email="alex@example.com", password_hash="pw")
    group = Group(group_name="admins", description="Admin group")
    lang = Language(language_code="en", language_name="English")
    category = Category(name="Vegetables")
    ingredient = Ingredient(name="Tomato")
    unit = Unit(symbol="g")
    ingredient.categories.append(category)

    # Add base objects and getting ids
    session.add_all([user, group, lang, category, ingredient, unit])
    session.flush()

    # Groups
    user_group = UserGroup(
        user_id=user.id,
        group_id=group.id)

    # Recipe
    recipe = Recipe(
        author_id=user.id,
        cooking_time_in_minutes=15)

    # Translations
    ingredient_translation = IngredientTranslation(
        ingredient_id=ingredient.id,
        language_id=lang.id
    )

    # Add another objects and getting ids
    session.add_all([recipe, user_group, ingredient_translation])
    session.flush()

    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient.id,
        language_id=lang.id,
        quantity=100
    )
    session.add(recipe_ingredient)

    # User recipe
    user_recipe = UserRecipe(
        base_recipe_id=recipe.id,
        user_id=user.id,
        language_id=lang.id,
        title="My Tomato Salad",
        description="Custom description",
        instructions="Cut and serve"
    )
    session.add(user_recipe)
    session.flush()

    recipe_translation = RecipeTranslation(
        recipe_id=recipe.id,
        language_id=lang.id,
        title="Tomato Salad",
        description="Fresh salad"
    )
    unit_translation = UnitTranslation(
        unit_id=unit.id,
        language_id=lang.id,
        symbol="grams"
    )

    user_recipe_ingredient = UserRecipeIngredient(
        user_recipe_id=user_recipe.id,
        ingredient_id=ingredient.id,
        unit_id=unit.id,
        language_id=lang.id,
        quantity=100
    )

    session.add_all([user_recipe_ingredient, unit_translation, recipe_translation])
    session.commit()

    return {
        "user": user,
        "group": group,
        "lang": lang,
        "ingredient": ingredient,
        "category": category,
        "unit": unit,
        "recipe": recipe,
        "user_recipe": user_recipe
    }


def test_user_groups(sample_data, session):
    user = sample_data["user"]
    group = sample_data["group"]
    assert group in user.groups
    assert user in group.users


def test_recipe_author_and_ingredients(sample_data, session):
    recipe = sample_data["recipe"]
    user = sample_data["user"]
    ingredient = sample_data["ingredient"]

    assert recipe.author == user
    assert ingredient in recipe.ingredients
    assert recipe in ingredient.recipes


def test_category_ingredient(sample_data, session):
    ingredient = sample_data["ingredient"]
    category = sample_data["category"]
    assert category in ingredient.categories
    assert ingredient in category.ingredients


def test_translations(sample_data, session):
    lang = sample_data["lang"]
    ingredient = sample_data["ingredient"]
    recipe = sample_data["recipe"]
    unit = sample_data["unit"]

    assert any(t.language == lang for t in ingredient.translations)
    assert any(t.language == lang for t in recipe.translations)
    assert any(t.language == lang for t in unit.translations)


def test_user_recipe_and_links(sample_data, session):
    user_recipe = sample_data["user_recipe"]
    recipe = sample_data["recipe"]
    user = sample_data["user"]

    assert user_recipe.base_recipe == recipe
    assert user_recipe.user == user
    assert any(ing.ingredient.name == "Tomato" for ing in user_recipe.ingredients)

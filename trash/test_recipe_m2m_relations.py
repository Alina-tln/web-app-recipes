import pytest
from sqlalchemy import select
from recipe_service.models.recipes import Recipe, RecipeIngredient, UserRecipeIngredient
from translation_service.models.translations import Language

@pytest.mark.asyncio
async def test_recipe_ingredient_multi_schema_m2m_linkage(
        async_session, setup_base_dependencies, recipe_data
):
    """
    Проверка установления M:M связи через RecipeIngredient,
    а также доступности связанных объектов Language и Unit.
    """
    deps = setup_base_dependencies

    # 1. Создание Recipe
    recipe = Recipe(author_id=deps['user_id'], **recipe_data)
    async_session.add(recipe)
    await async_session.flush()

    # 2. Создание RecipeIngredient (используем ID из 4-х таблиц, 3-х схем)
    ri = RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=deps['ingredient_id'],
        quantity=150.0,
        unit_id=deps['unit_id'],
        language_id=deps['language_id']
    )
    async_session.add(ri)
    await async_session.commit()

    # 3. Проверка: Доступ к связанным объектам (проверка, что ORM-отношения работают)

    await async_session.refresh(ri)

    # Проверка Language (cross-schema)
    assert ri.language.language_code == deps['language'].language_code

    # Проверка Unit (same-schema, different table)
    assert ri.unit.symbol == deps['unit'].symbol
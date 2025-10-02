import pytest
from sqlalchemy import select
from recipe_service.models.recipes import Recipe
from translation_service.models.translations import RecipeTranslation

@pytest.mark.asyncio
async def test_recipe_deletion_cascades_to_recipe_translation(
        async_session, setup_base_dependencies, recipe_data
):
    """
    Проверка межсхемной связи: Recipe (recipes) -> RecipeTranslation (translations) с ondelete="CASCADE".
    """
    deps = setup_base_dependencies

    # 1. Создание Recipe и связанного перевода
    recipe = Recipe(author_id=deps['user_id'], **recipe_data)
    async_session.add(recipe)
    await async_session.flush()

    translation = RecipeTranslation(
        recipe_id=recipe.id,
        language_id=deps['language_id'],
        title="Test Recipe Title",
        description="Desc",
        instructions="Instr"
    )
    async_session.add(translation)
    await async_session.commit()
    translation_id = translation.id

    # 2. Удаление Recipe
    await async_session.delete(recipe)
    await async_session.commit()

    # 3. Проверка: перевод должен быть удален
    stmt_trans = select(RecipeTranslation).where(RecipeTranslation.id == translation_id)
    deleted_translation = (await async_session.execute(stmt_trans)).scalar_one_or_none()

    assert deleted_translation is None, "RecipeTranslation не был удален каскадно."
import pytest
from sqlalchemy import select
from recipe_service.models.ingredients import Ingredient
from translation_service.models.translations import IngredientTranslation

@pytest.mark.asyncio
async def test_ingredient_deletion_cascades_to_translation(
        async_session,
):
    """
    Проверка межсхемной связи: Ingredient (recipes) -> IngredientTranslation (translations)
    с ondelete="CASCADE" на ingredient_id.
    """
    deps = setup_base_dependencies

    # 1. Создание Ingredient
    ingredient = deps['ingredient'] # Берем из фикстуры
    ing_id = ingredient.id

    # 2. Создание IngredientTranslation (связь с Language из другой схемы)
    translation = IngredientTranslation(
        ingredient_id=ing_id,
        language_id=deps['language_id']
    )
    async_session.add(translation)
    await async_session.commit()
    translation_id = translation.id

    # 3. Удаление Ingredient
    await async_session.delete(ingredient)
    await async_session.commit()

    # 4. Проверка: перевод должен быть удален каскадно
    stmt_trans = select(IngredientTranslation).where(IngredientTranslation.id == translation_id)
    deleted_translation = (await async_session.execute(stmt_trans)).scalar_one_or_none()

    assert deleted_translation is None, "IngredientTranslation не был удален каскадно."
from translation_service.models.translations import Language, IngredientTranslation, RecipeTranslation, UnitTranslation

# ----------------- Тесты для Language -----------------

def test_language_model_metadata():
    """Проверка имени таблицы и схемы для Language."""
    assert Language.__tablename__ == 'languages'
    assert Language.__table_args__[-1]['schema'] == 'translations'

def test_language_unique_constraints():
    """Проверка уникальных ограничений на language_code и language_name."""

    # 1. Проверка UniqueConstraint на language_code (установлен в __table_args__)
    # Если UniqueConstraint задан в кортеже __table_args__, его нужно найти:
    constraints = Language.__table__.constraints
    found_uq_code = False

    for constraint in constraints:
        if str(constraint.name) == 'uq_language_code': # Проверяем имя, если оно задано
            cols = {c.name for c in constraint.columns}
            assert 'language_code' in cols
            found_uq_code = True
            break

    # NOTE: В модели Language UniqueConstraint задан как 'UniqueConstraint("language_code")'
    # Проверим более простой путь: свойство .unique на самой колонке (для language_name)

    # 2. Проверка .unique на колонке language_name
    name_col = Language.__table__.columns['language_name']
    assert name_col.unique is True
    assert Language.__table__.columns['language_code'].unique is True

    # Поскольку 'language_code' и 'language_name' объявлены как unique=True,
    # проверка атрибутов колонок наиболее проста.

def test_language_repr():
    """Проверка корректности метода __repr__ для Language."""
    lang = Language(id=1, language_code='ru', language_name='Russian')
    expected_repr = "<Language(id=1, code='ru', name='Russian')>"
    assert repr(lang) == expected_repr

# ----------------- Тесты для IngredientTranslation -----------------

def test_ingredient_translation_model_metadata():
    """Проверка имени таблицы и схемы для IngredientTranslation."""
    assert IngredientTranslation.__tablename__ == 'ingredient_translations'
    assert IngredientTranslation.__table_args__[-1]['schema'] == 'translations' # Здесь у нас кортеж

def test_ingredient_translation_unique_constraint():
    """Проверка составного уникального ограничения uq_ingredient_translation."""

    constraints = IngredientTranslation.__table__.constraints
    found = False
    for constraint in constraints:
        if str(constraint.name) == 'uq_ingredient_translation':
            found = True
            cols = {c.name for c in constraint.columns}
            assert 'ingredient_id' in cols
            assert 'language_id' in cols
            break

    assert found, "UniqueConstraint 'uq_ingredient_translation' не найден."

# ----------------- Тесты для RecipeTranslation -----------------

def test_recipe_translation_model_metadata():
    """Проверка имени таблицы и схемы для RecipeTranslation."""
    assert RecipeTranslation.__tablename__ == 'recipe_translations'
    assert RecipeTranslation.__table_args__[-1]['schema'] == 'translations' # Здесь у нас кортеж

def test_recipe_translation_unique_constraint():
    """Проверка составного уникального ограничения uq_recipe_translation."""

    constraints = RecipeTranslation.__table__.constraints
    found = False
    for constraint in constraints:
        if str(constraint.name) == 'uq_recipe_translation':
            cols = {c.name for c in constraint.columns}
            assert 'recipe_id' in cols
            assert 'language_id' in cols
            found = True
            break

    assert found, "UniqueConstraint 'uq_recipe_translation' не найден."

def test_recipe_translation_repr():
    """Проверка корректности метода __repr__ для RecipeTranslation."""
    rt = RecipeTranslation(id=10, recipe_id=101, language_id=1, title='Pizza')
    expected_repr = "<RecipeTranslation(id=10, recipe_id=101, lang_id=1, title='Pizza')>"
    assert repr(rt) == expected_repr

# ----------------- Тесты для UnitTranslation -----------------

def test_unit_translation_model_metadata():
    """Проверка имени таблицы и схемы для UnitTranslation."""
    assert UnitTranslation.__tablename__ == 'unit_translations'
    assert UnitTranslation.__table_args__[-1]['schema'] == 'translations' # Здесь у нас кортеж

def test_unit_translation_unique_constraint():
    """Проверка составного уникального ограничения uq_unit_translation."""

    constraints = UnitTranslation
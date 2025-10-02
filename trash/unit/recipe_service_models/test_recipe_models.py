from recipe_service.models.recipes import  Recipe, RecipeIngredient, UserRecipe, UserRecipeIngredient, Unit

# ----------------- Тесты для Recipe -----------------

def test_recipe_model_metadata():
    """Проверка имени таблицы и схемы для Recipe."""
    assert Recipe.__tablename__ == 'recipes'
    assert Recipe.__table_args__['schema'] == 'recipes'

def test_recipe_model_columns():
    """Проверка наличия ключевых колонок в Recipe."""
    columns = Recipe.__table__.columns
    assert 'id' in columns
    assert 'author_id' in columns
    assert 'cooking_time_in_minutes' in columns
    assert 'created_at' in columns
    assert 'updated_at' in columns

def test_recipe_repr():
    """Проверка корректности метода __repr__ для Recipe."""
    recipe = Recipe(id=1, author_id=101, cooking_time_in_minutes=45)
    expected_repr = "<Recipe(id=1, author_id=101, cooking_time=45)>"
    assert repr(recipe) == expected_repr

# ----------------- Тесты для RecipeIngredient -----------------

def test_recipe_ingredient_model_metadata():
    """Проверка имени таблицы и схемы для RecipeIngredient."""
    assert RecipeIngredient.__tablename__ == 'recipe_ingredients'
    assert RecipeIngredient.__table_args__['schema'] == 'recipes'

def test_recipe_ingredient_primary_keys():
    """Проверка составного первичного ключа RecipeIngredient."""
    pk_cols = RecipeIngredient.__table__.primary_key.columns.keys()
    assert set(pk_cols) == {'recipe_id', 'ingredient_id'}

# ----------------- Тесты для UserRecipe -----------------

def test_user_recipe_model_metadata():
    """Проверка имени таблицы и схемы для UserRecipe."""
    assert UserRecipe.__tablename__ == 'user_recipes'
    assert UserRecipe.__table_args__['schema'] == 'recipes'

def test_user_recipe_repr():
    """Проверка корректности метода __repr__ для UserRecipe."""
    ur = UserRecipe(id=1, user_id=10, base_recipe_id=5, title='My Pasta')
    expected_repr = "<UserRecipe(id=1, user_id=10, base_recipe_id=5, title='My Pasta')>"
    assert repr(ur) == expected_repr

# ----------------- Тесты для UserRecipeIngredient -----------------

def test_user_recipe_ingredient_model_metadata():
    """Проверка имени таблицы и схемы для UserRecipeIngredient."""
    assert UserRecipeIngredient.__tablename__ == 'user_recipe_ingredients'
    assert UserRecipeIngredient.__table_args__['schema'] == 'recipes'

def test_user_recipe_ingredient_primary_keys():
    """Проверка составного первичного ключа UserRecipeIngredient."""
    pk_cols = UserRecipeIngredient.__table__.primary_key.columns.keys()
    assert set(pk_cols) == {'user_recipe_id', 'ingredient_id'}

# ----------------- Тесты для Unit -----------------

def test_unit_model_metadata():
    """Проверка имени таблицы и схемы для Unit."""
    assert Unit.__tablename__ == 'units'
    assert Unit.__table_args__['schema'] == 'recipes'

def test_unit_unique_constraint():
    """Проверка, что symbol в Unit является уникальным."""
    symbol_col = Unit.__table__.columns['symbol']
    assert symbol_col.unique is True

def test_unit_repr():
    """Проверка корректности метода __repr__ для Unit."""
    unit = Unit(id=1, symbol='ml')
    expected_repr = "<Unit(id=1, symbol='ml')>"
    assert repr(unit) == expected_repr
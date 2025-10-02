from recipe_service.models.ingredients import Ingredient, Category, IngredientCategory

# ----------------- Тесты для Ingredient -----------------

def test_ingredient_model_metadata():
    """Проверка имени таблицы и схемы для Ingredient."""
    assert Ingredient.__tablename__ == 'ingredients'
    assert Ingredient.__table_args__['schema'] == 'recipes'

def test_ingredient_repr():
    """Проверка корректности метода __repr__ для Ingredient."""
    ingredient = Ingredient(id=10, name='Salt')
    expected_repr = "<Ingredient(id=10, name='Salt')>"
    assert repr(ingredient) == expected_repr

# ----------------- Тесты для Category -----------------

def test_category_model_metadata():
    """Проверка имени таблицы и схемы для Category."""
    assert Category.__tablename__ == 'categories'
    assert Category.__table_args__['schema'] == 'recipes'

def test_category_unique_constraint():
    """Проверка, что name в Category является уникальным."""
    name_col = Category.__table__.columns['name']
    assert name_col.unique is True

def test_category_repr():
    """Проверка корректности метода __repr__ для Category."""
    category = Category(id=1, name='Spices')
    expected_repr = "<Category(id=1, name='Spices')>"
    assert repr(category) == expected_repr

# ----------------- Тесты для IngredientCategory -----------------

def test_ingredient_category_model_metadata():
    """Проверка имени таблицы и схемы для IngredientCategory."""
    assert IngredientCategory.__tablename__ == 'ingredient_categories'
    assert IngredientCategory.__table_args__['schema'] == 'recipes'

def test_ingredient_category_primary_keys():
    """Проверка составного первичного ключа IngredientCategory."""
    pk_cols = IngredientCategory.__table__.primary_key.columns.keys()
    assert set(pk_cols) == {'ingredient_id', 'category_id'}

def test_ingredient_category_repr():
    """Проверка корректности метода __repr__ для IngredientCategory."""
    ic = IngredientCategory(ingredient_id=5, category_id=1)
    expected_repr = "<IngredientCategory(ingredient_id=5, category_id=1)>"
    assert repr(ic) == expected_repr

from user_service.models.users import User


def test_user_model_metadata():
    """
    Проверка, что модель User корректно определена:
    1. Имя таблицы.
    2. Имя схемы.
    """
    assert User.__tablename__ == 'users'
    # Проверка __table_args__ для схемы (обычно это последний элемент кортежа)
    assert User.__table_args__[-1]['schema'] == 'users'

def test_user_model_columns_exist():
    """
    Проверка наличия всех ключевых колонок в таблице.
    """
    columns = User.__table__.columns
    assert 'id' in columns
    assert 'username' in columns
    assert 'email' in columns
    assert 'password_hash' in columns
    assert 'oauth_id' in columns
    assert 'provider_name' in columns
    assert 'is_verified' in columns
    assert 'created_at' in columns

def test_user_unique_constraint():
    """
    Проверка составного уникального ограничения для OAuth.
    UniqueConstraint("oauth_id", "provider_name", name="uq_user_oauth")
    """

    # SQLAlchemy хранит ограничения в __table__.constraints
    constraints = User.__table__.constraints

    found = False
    for constraint in constraints:
        # Ищем по имени
        if str(constraint.name) == 'uq_user_oauth':
            found = True
            # Проверяем, что ограничение включает нужные колонки
            cols = {c.name for c in constraint.columns}
            assert 'oauth_id' in cols
            assert 'provider_name' in cols
            break

    assert found, "UniqueConstraint 'uq_user_oauth' не найден."



#TODO
# def test_user_repr(test_user_fixture):
#     """
#     Проверка корректности метода __repr__.
#     """
#     # Создаем экземпляр модели, используя фикстурные данные, но не сохраняем в БД.
#     user_instance = User(id=1, **test_user_fixture)
#
#     # Ожидаемый результат: <User(id=1, email='test@example.com')>
#     expected_repr = f"<User(id={user_instance.id}, email='{test_user_fixture['email']}')>"
#
#     assert repr(user_instance) == expected_repr
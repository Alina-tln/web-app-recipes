from user_service.models.groups import Group, UserGroup

# ----------------- Тесты для Group -----------------

def test_group_model_metadata():
    """
    Проверка имени таблицы и схемы для Group.
    """
    assert Group.__tablename__ == 'groups'
    assert Group.__table_args__['schema'] == 'users'

def test_group_unique_constraint():
    """
    Проверка, что group_name является уникальным.
    """
    group_name_col = Group.__table__.columns['group_name']
    assert group_name_col.unique is True
    assert group_name_col.nullable is False

def test_group_repr():
    """
    Проверка корректности метода __repr__ для Group.
    """
    group_instance = Group(id=5, group_name='Admins')
    expected_repr = "<Group(id=5, group_name='Admins')>"
    assert repr(group_instance) == expected_repr

# ----------------- Тесты для UserGroup -----------------

def test_usergroup_model_metadata():
    """
    Проверка имени таблицы и схемы для UserGroup.
    """
    assert UserGroup.__tablename__ == 'user_groups'
    assert UserGroup.__table_args__['schema'] == 'users'

def test_usergroup_primary_keys():
    """
    Проверка составного первичного ключа.
    """
    # Primary key должен включать user_id и group_id
    pk_cols = UserGroup.__table__.primary_key.columns.keys()
    assert set(pk_cols) == {'user_id', 'group_id'}

def test_usergroup_repr():
    """
    Проверка корректности метода __repr__ для UserGroup.
    """
    ug_instance = UserGroup(user_id=10, group_id=20)
    expected_repr = "<UserGroup(user_id=10, group_id=20)>"
    assert repr(ug_instance) == expected_repr
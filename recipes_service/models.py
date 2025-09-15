from enum import unique

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    __table_args__ = {"schema": "recipes"}

    id = db.Column(db.BigInteger, primary_key=True)
    common_name = db.Column(db.Text, unique=True, nullable=False)

class IngredientCategory(db.Model):
    __tablename__ = "ingredient_categories"
    __table_args__ = {"schema": "recipes"}

    id = db.Column(db.BigInteger, primary_key=True)
    category_name = db.Column(db.Text, unique=True, nullable=False)

class IngredientCategoryMapping(db.Model):
    __tablename__ = "ingredient_category_mappings"
    __table_args__ = {"schema": "recipes"}

    ingredient_id = db.Column(db.BigInteger, foreign_key="ingredients.id", primary_key=True, ondelete="CASCADE")
    category_id = db.Column(db.BigInteger, foreign_key="ingredient_categories.id", primary_key=True, ondelete="CASCADE")

class Recipe(db.Model):
    __tablename__ = "recipes"
    __table_args__ = {"schema": "recipes"}

    id = db.Column(db.BigInteger, primary_key=True)
    author_id = db.Column(db.BigInteger, foreign_key="users.users.id", ondelete="CASCADE") #Todo nullable=False, when users api will be ready
    cooking_time_in_minutes = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(),onupdate=db.func.now())

class RecipeIngredients(db.Model):
    __tablename__ = "recipe_ingredients"
    __table_args__ = {"schema": "recipes"}

    recipe_id = db.Column(db.BigInteger, foreign_key="recipes.id", primary_key=True, ondelete="CASCADE")
    ingredient_id = db.Column(db.BigInteger, foreign_key="ingredients.id", nullable=False, primary_key=True, ondelete="CASCADE")
    quantity = db.Column(db.Decimal)
    unit = db.Column(db.Text)
    language_code = db.Column(db.varchar(5), primary_key=True, nullable=False)

class UserRecipes(db.Model):
    __tablename__ = "user_recipes"
    __table_args__ = {"schema": "recipes"}

    id = db.Column(db.BigInteger, primary_key=True)
    base_recipe_id = db.Column(db.BigInteger, foreign_key="recipes.id", nullable=False, ondelete="CASCADE", unique=True)
    user_id = db.Column(db.BigInteger, foreign_key="users.id", nullable=False, unique=True) ##Todo nullable=False, when users api will be ready
    language_code = db.Column(db.varchar(5), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.varchar(100), nullable=False)
    description = db.Column(db.varchar(250))
    instructions = db.Column(db.Text, nullable=False)

class UserRecipeIngredients(db.Model):
    __tablename__ = "user_recipe_ingredients"
    __table_args__ = {"schema": "recipes"}

    user_recipe_id = db.Column(db.BigInteger, foreign_key="user_recipes.id", nullable=False, ondelete="CASCADE", unique=True)
    ingredient_id = db.Column(db.BigInteger, foreign_key="ingredients.id", nullable=False, unique=True)
    quantity = db.Column(db.Decimal)
    unit = db.Column(db.Text)
    language_code = db.Column(db.varchar(5), nullable=False, unique=True)
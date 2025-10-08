from sqlalchemy import Column, BigInteger, String, ForeignKey
from db_base import Base
from .recipes_models import RecipeIngredient
from sqlalchemy.orm import relationship

class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"
    __table_args__ = {"schema": "recipes"}

    ingredient_id = Column(BigInteger, ForeignKey("recipes.ingredients.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(BigInteger, ForeignKey("recipes.categories.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        return f"<IngredientCategory(ingredient_id={self.ingredient_id}, category_id={self.category_id})>"


class Ingredient(Base):
    __tablename__ = "ingredients"
    __table_args__ = {"schema": "recipes"}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)

    #Relationship for ORM
    categories = relationship("Category", secondary=IngredientCategory.__table__, back_populates="ingredients")
    recipes = relationship("Recipe", secondary=RecipeIngredient.__table__, back_populates="ingredients")
    user_recipes = relationship("UserRecipeIngredient", back_populates="ingredient")
    translations = relationship("IngredientTranslation", back_populates="ingredient")

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}')>"


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "recipes"}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    #Relationship for ORM
    ingredients = relationship("Ingredient", secondary=IngredientCategory.__table__, back_populates="categories")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"





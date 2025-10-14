from sqlalchemy import Column, BigInteger, String, ForeignKey
from db_base import Base
from sqlalchemy.orm import relationship


class IngredientCategory(Base):
    __tablename__ = "ingredient_categories"
    __table_args__ = {"schema": "recipes"}

    ingredient_id = Column(BigInteger,
                           ForeignKey("recipes.ingredients.id", ondelete="CASCADE"),
                           primary_key=True)
    category_id = Column(BigInteger,
                         ForeignKey("recipes.categories.id", ondelete="CASCADE"),
                         primary_key=True)

    def __repr__(self):
        return (f"<IngredientCategory(ingredient_id={self.ingredient_id}, "
                f"category_id={self.category_id})>")


class Ingredient(Base):
    __tablename__ = "ingredients"
    __table_args__ = {"schema": "recipes"}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationship for ORM
    categories = relationship("Category",
                              secondary="recipes.ingredient_categories",
                              back_populates="ingredients",
                              lazy="selectin"
                              )
    recipes = relationship("Recipe",
                           secondary="recipes.recipe_ingredients",
                           back_populates="ingredients"
                           )
    user_recipes = relationship("UserRecipeIngredient",
                                back_populates="ingredient"
                                )

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name={self.name!r})>"


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "recipes"}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship for ORM
    ingredients = relationship("Ingredient",
                               secondary=IngredientCategory.__table__,
                               back_populates="categories"
                               )

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name!r})>"

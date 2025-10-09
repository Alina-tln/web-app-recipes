from typing import Any

from db_base import Base
from sqlalchemy import Column, BigInteger, ForeignKey, Text, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Language(Base):
    __tablename__ = "languages"
    __table_args__ = (UniqueConstraint("language_code"),
                      {"schema": "translations"}
                      )

    id = Column(BigInteger, primary_key=True)
    language_code = Column(String(5), unique=True, nullable=False)
    language_name = Column(String(100), nullable=False, unique=True)

    recipe_ingredients = relationship("RecipeIngredient", back_populates="language")
    user_recipe_ingredients = relationship(
        "UserRecipeIngredient",
        back_populates="language")
    ingredient_translations = relationship(
        "IngredientTranslation",
        back_populates="language")
    user_recipes = relationship("UserRecipe", back_populates="language")
    recipe_translations = relationship("RecipeTranslation", back_populates="language")
    unit_translations = relationship("UnitTranslation", back_populates="language")

    def __repr__(self):
        return (f"<Language(id={self.id}, code={self.language_code!r}"
                f", name={self.language_name!r})>")


class IngredientTranslation(Base):
    __tablename__ = "ingredient_translations"
    __table_args__ = (
        UniqueConstraint(
            "ingredient_id",
            "language_id",
            name="uq_ingredient_translation"),
        {"schema": "translations"}
    )

    id = Column(BigInteger, primary_key=True)
    ingredient_id = Column(
        BigInteger,
        ForeignKey("recipes.ingredients.id", ondelete="CASCADE"),
        nullable=False)
    language_id = Column(
        BigInteger,
        ForeignKey("translations.languages.id"),
        nullable=False)

    ingredient = relationship("Ingredient", back_populates="translations")
    language = relationship("Language", back_populates="ingredient_translations")

    def __repr__(self):
        return (f"<IngredientTranslation(id={self.id}, "
                f"ingredient_id={self.ingredient_id}, language_id={self.language_id})>")


class RecipeTranslation(Base):
    __tablename__ = "recipe_translations"
    __table_args__ = (
        UniqueConstraint("recipe_id", "language_id", name="uq_recipe_translation"),
        {"schema": "translations"}
    )

    id = Column(BigInteger, primary_key=True)
    recipe_id = Column(
        BigInteger,
        ForeignKey("recipes.recipes.id", ondelete="CASCADE"),
        nullable=False)
    language_id = Column(
        BigInteger,
        ForeignKey("translations.languages.id", ondelete="CASCADE"),
        nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    instructions = Column(Text)

    recipe = relationship("Recipe", back_populates="translations")
    language = relationship("Language", back_populates="recipe_translations")

    def __repr__(self):
        return (f"<RecipeTranslation(id={self.id}, recipe_id={self.recipe_id}, "
                f"lang_id={self.language_id}, title={self.title!r})>")


class UnitTranslation(Base):
    __tablename__ = 'unit_translations'
    __table_args__ = (
        UniqueConstraint("unit_id", "language_id", name="uq_unit_translation"),
        {"schema": "translations"}
    )

    id = Column(BigInteger, primary_key=True)
    unit_id = Column(BigInteger, ForeignKey("recipes.units.id"), nullable=False)
    language_id = Column(
        BigInteger,
        ForeignKey("translations.languages.id"),
        nullable=False)
    symbol = Column(String(10), nullable=False)

    unit = relationship("Unit", back_populates="translations")
    language = relationship("Language", back_populates="unit_translations")

    def __init__(self, **kw: Any):
        super().__init__(**kw)
        self.name = None

    def __repr__(self):
        return (f"<UnitTranslation(id={self.id}, unit_id={self.unit_id}, "
                f"lang_id={self.language_id}, name={self.name!r})>")

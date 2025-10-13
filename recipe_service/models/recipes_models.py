from db_base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    Integer,
    Text,
    TIMESTAMP,
    func,
    String,
    Float)


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = {"schema": "recipes"}
    __mapper_args__ = {"confirm_deleted_rows": False}

    recipe_id = Column(
        BigInteger,
        ForeignKey("recipes.recipes.id", ondelete="CASCADE"),
        primary_key=True
    )
    ingredient_id = Column(
        BigInteger,
        ForeignKey("recipes.ingredients.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
    quantity = Column(Float, nullable=False)
    unit_id = Column(BigInteger, ForeignKey("recipes.units.id"), nullable=True)
    language_id = Column(
        BigInteger,
        ForeignKey("translations.languages.id"),
        nullable=False
    )

    unit = relationship("Unit", back_populates="recipe_ingredients")
    language = relationship("Language", back_populates="recipe_ingredients")

    def __repr__(self):
        return (f"<RecipeIngredient(recipe_id={self.recipe_id}, "
                f"ingredient_id={self.ingredient_id}, quantity={self.quantity})>")


class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = {"schema": "recipes"}

    id = Column(BigInteger, primary_key=True)
    author_id = Column(
        BigInteger,
        ForeignKey("users.users.id", ondelete="SET NULL"),
        nullable=True
    )
    cooking_time_in_minutes = Column(Integer)
    image_url = Column(String(1000))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    author = relationship("User", back_populates="recipes")
    ingredients = relationship(
        "Ingredient",
        secondary=RecipeIngredient.__table__,
        back_populates="recipes")
    user_recipes = relationship("UserRecipe", back_populates="base_recipe")
    translations = relationship(
        "RecipeTranslation",
        back_populates="recipe"
    )

    def __repr__(self):
        return (f"<Recipe(id={self.id}, author_id={self.author_id}, "
                f"cooking_time={self.cooking_time_in_minutes})>")


class UserRecipe(Base):
    __tablename__ = "user_recipes"
    __table_args__ = {'schema': 'recipes'}

    id = Column(BigInteger, primary_key=True)
    base_recipe_id = Column(
        BigInteger,
        ForeignKey("recipes.recipes.id"),
        nullable=False
    )
    user_id = Column(BigInteger, ForeignKey("users.users.id"), nullable=False)
    language_id = Column(
        BigInteger,
        ForeignKey("translations.languages.id"),
        nullable=False)
    cooking_time_in_minutes = Column(Integer)
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    instructions = Column(Text, nullable=False)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships to User Service
    base_recipe = relationship("Recipe", back_populates="user_recipes")
    user = relationship("User", back_populates="user_recipes")
    language = relationship(
        "Language",
        back_populates="user_recipes"
    )
    ingredients = relationship("UserRecipeIngredient", back_populates="user_recipe")

    def __repr__(self):
        return (f"<UserRecipe(id={self.id}, user_id={self.user_id}, "
                f"base_recipe_id={self.base_recipe_id}, title={self.title!r})>")


class UserRecipeIngredient(Base):
    __tablename__ = "user_recipe_ingredients"
    __table_args__ = {"schema": "recipes"}
    __mapper_args__ = {"confirm_deleted_rows": False}

    user_recipe_id = Column(
        BigInteger,
        ForeignKey("recipes.user_recipes.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True
    )
    ingredient_id = Column(
        BigInteger,
        ForeignKey("recipes.ingredients.id"),
        nullable=False,
        primary_key=True
    )
    quantity = Column(Float, nullable=False)
    unit_id = Column(BigInteger, ForeignKey("recipes.units.id"), nullable=True)
    language_id = Column(
        BigInteger,
        ForeignKey("translations.languages.id"),
        nullable=False
    )

    user_recipe = relationship("UserRecipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="user_recipes")
    language = relationship("Language", back_populates="user_recipe_ingredients")
    unit = relationship("Unit", back_populates="user_recipe_ingredients")

    def __repr__(self):
        return (f"<UserRecipeIngredient(user_recipe_id={self.user_recipe_id}, "
                f"ingredient_id={self.ingredient_id}, quantity={self.quantity})>"
                )


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = {"schema": "recipes"}

    id = Column(BigInteger, primary_key=True)
    symbol = Column(String(10), nullable=False, unique=True)

    translations = relationship("UnitTranslation", back_populates="unit")
    user_recipe_ingredients = relationship(
        "UserRecipeIngredient",
        back_populates="unit"
    )
    recipe_ingredients = relationship("RecipeIngredient", back_populates="unit")

    def __repr__(self):
        return f"<Unit(id={self.id}, symbol={self.symbol!r})>"

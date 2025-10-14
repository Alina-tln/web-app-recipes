from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict


# ----------------------------------------------------------
# Recipe Schemas
# ----------------------------------------------------------
class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RecipeSchema(BaseSchema):
    cooking_time_in_minutes: int | None = Field(default=None, ge=0, le=1200)
    image_url: str | None = Field(default=None, max_length=1000)


class RecipeCreateSchema(RecipeSchema):
    author_id: int | None = Field(default=None)
    ingredient_ids: List[int] = Field(default_factory=list)


class RecipeUpdateSchema(BaseSchema):
    cooking_time_in_minutes: int | None = Field(default=None, ge=0, le=1200)
    image_url: str | None = Field(default=None, max_length=1000)
    ingredient_ids: List[int] = Field(default_factory=list)


class RecipeReadSchema(RecipeSchema):
    id: int
    author_id: int | None = Field(default=None)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------
# Recipe Ingredient Schemas
# ----------------------------------------------------------
class RecipeIngredientSchema(BaseSchema):
    recipe_id: int
    ingredient_id: int
    quantity: float = Field(gt=0)
    unit_id: int | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------
# User Recipe Schemas
# ----------------------------------------------------------
class UserRecipeSchema(BaseSchema):
    cooking_time_in_minutes: int | None = Field(default=None, ge=0, le=1200)
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    instructions: str


class UserRecipeCreateSchema(UserRecipeSchema):
    base_recipe_id: int
    user_id: int


class UserRecipeReadSchema(UserRecipeSchema):
    id: int
    base_recipe_id: int
    user_id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------
# User Recipe Ingredient Schemas
# ----------------------------------------------------------
class UserRecipeIngredientSchema(BaseSchema):
    user_recipe_id: int
    ingredient_id: int
    quantity: float = Field(gt=0)
    unit_id: int | None = Field(default=None)


# ----------------------------------------------------------
# Unit Schema
# ----------------------------------------------------------
class UnitSchema(BaseSchema):
    id: int | None = Field(default=None)
    symbol: str = Field(max_length=10)

    model_config = ConfigDict(from_attributes=True)

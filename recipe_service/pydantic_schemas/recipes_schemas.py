from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from recipe_service.examples.recipe_examples import recipe_examples


# ----------------------------------------------------------
# Recipe Schemas
# ----------------------------------------------------------
class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RecipeSchema(BaseSchema):
    cooking_time_in_minutes: int | None = Field(default=None, ge=0, le=1200, examples=[60])
    image_url: str | None = Field(max_length=1000, examples=["http://example.com/image.jpg"])


class RecipeIngredientSchema(BaseSchema):
    ingredient_id: int = Field(description="Ingredient ID", examples=[1])
    quantity: float = Field(
        gt=0,
        description="Ingredient id",
        examples=["15"])
    unit_id: int | None = Field(default=None, description="Unit ID", examples=[1])


class RecipeCreateSchema(RecipeSchema):
    ingredients: List[RecipeIngredientSchema] = Field(default_factory=list)


class RecipeUpdateSchema(RecipeSchema):
    ingredients: List[RecipeIngredientSchema] | None = Field(default=None)


class RecipeReadSchema(BaseSchema):
    id: int = Field(description="Recipe ID", examples=[1])
    author_id: int | None = Field(default=None, description="Author's ID", examples=[1])
    cooking_time_in_minutes: int | None = Field(default=None, ge=0, le=1200, examples=[60])
    image_url: str | None = Field(default=None, max_length=1000, examples=["http://example.com/image.jpg"])
    ingredients: List[RecipeIngredientSchema] | None = Field(default=None)
    created_at: datetime
    updated_at: datetime

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


class UserRecipeReadSchema(BaseSchema):
    id: int
    base_recipe_id: int
    user_id: int
    updated_at: datetime
    cooking_time_in_minutes: int | None = Field(default=None, ge=0, le=1200)
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    instructions: str

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


# ----------------------------------------------------------
#  Delete Response Schema
# ----------------------------------------------------------
class DeleteResponseSchema(BaseModel):
    Result: bool
    id: int
    name: str | None = Field(default=None)

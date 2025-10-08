from typing import List

from pydantic import BaseModel, Field, ConfigDict, constr


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

# ----------------------------------------------------------
# Category Schemas
# ----------------------------------------------------------

class CategoryCreateSchema(BaseSchema):
    name: constr(min_length=2, max_length=100) = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Category name",
        examples=["Fruits"]
    )

class CategoryUpdateSchema(BaseSchema):
    name: constr(min_length=2, max_length=100) | None = Field(
        default=None,
        max_length=100,
        examples=["Fruits"],
        description="New category name"
    )

class CategoryReadSchema(BaseSchema):
    id: int = Field(..., examples=[1])
    name: constr(min_length=2, max_length=100) = Field(..., examples=["Fruits"])


# ----------------------------------------------------------
# Ingredient Schemas
# ----------------------------------------------------------
class IngredientCreateSchema(BaseSchema):
    name: constr(min_length=2, max_length=100) = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Ingredient name",
        examples=["Cheese"]
    )
    category_ids: List[int] = Field(..., examples=[1, 2])

class IngredientUpdateSchema(BaseSchema):
    name: constr(min_length=2, max_length=100) | None = Field(
        default=None,
        max_length=100,
        examples=["Mozzarella"],
        description="New ingredient name"
    )
    category_ids: List[int] | None = Field(default=None, examples=[2])

class IngredientReadSchema(BaseSchema):
    id: int = Field(..., examples=[1])
    name: constr(min_length=2, max_length=100) = Field(..., examples=["Fruits"])
    categories: List[str]


# ----------------------------------------------------------
# Delete Response Schemas
# ----------------------------------------------------------
class DeleteResponseSchema(BaseModel):
    Result: bool
    id: int
    name: str
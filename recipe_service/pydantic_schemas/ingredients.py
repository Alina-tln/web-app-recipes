from pydantic import BaseModel, Field, ConfigDict, constr


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

class IngredientSchema(BaseSchema):
    id: int | None = None
    name: str = Field(max_length=100)


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

class DeleteResponseSchema(BaseModel):
    Result: bool
    id: int
    name: str
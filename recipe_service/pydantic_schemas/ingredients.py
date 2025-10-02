from pydantic import BaseModel, Field, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

class IngredientSchema(BaseSchema):
    name: str = Field(max_length=100)


class CategorySchema(BaseSchema):
    name: str = Field(max_length=100)




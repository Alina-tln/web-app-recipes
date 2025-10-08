from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

class RecipeSchema(BaseSchema):
    author_id: int #todo Depended on users.users.id
    cooking_time_in_minutes: int = Field(ge=0, le=1200)
    image_url: str = Field(max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RecipeIngredientSchema(BaseSchema):
    recipe_id: int #todo Depended on recipes.recipes.id
    ingredient_id: int #todo Depended on recipes.ingredients.id
    quantity: float
    unit_id: int | None  #todo Depended on recipes.units.id
    language_id: int #todo Depended on translations.languages.id


class UserRecipeSchema(BaseSchema):
    base_recipe_id: int  #todo Depended on recipes.recipes.id
    user_id: int  #todo Depended on users.users.id
    language_id: int #todo Depended on translations.languages.id
    cooking_time_in_minutes: int = Field(ge=0, le=1200)
    title: str = Field(max_length=100)
    description: str | None = Field(max_length=1000)
    instructions: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRecipeIngredientSchema(BaseSchema):
    user_recipe_id: int #todo recipes.user_recipes.id
    ingredient_id: int #todo recipes.ingredients.id
    quantity: float
    unit_id: int | None  #todo Depended on recipes.units.id
    language_id: int #todo Depended on translations.languages.id

class UnitSchema(BaseSchema):
    symbol: str = Field(max_length=10)





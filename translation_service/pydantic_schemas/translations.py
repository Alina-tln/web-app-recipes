from pydantic import BaseModel, Field, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

class LanguageSchema(BaseSchema):
    language_code: str = Field(max_length=5)
    language_name: str = Field(max_length=100)

class IngredientTranslationSchema(BaseSchema):
    ingredient_id: int #todo Depended on recipes.ingredients.id
    language_id : int #todo Depended on translations.languages.id


class RecipeTranslationSchema(BaseSchema):
    recipe_id: int #todo Depended on recipes.recipes.id
    language_id: int #todo Depended on translations.languages.id
    title: str = Field(max_length=100)
    description: str = Field(max_length=1000)
    instructions: str


class UnitTranslationSchema(BaseSchema):
    unit_id: int #todo Depended on recipes.units.id
    language_id: int #todo Depended on translations.languages.id
    symbol: str = Field(max_length=10)
from pydantic import BaseModel, Field, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserGroupSchema(BaseSchema):
    user_id: int  # todo Depended on users.users.id
    group_id: int  # todo Depended on users.groups.id


class GroupsSchema(BaseSchema):
    group_name: str = Field(max_length=100)
    description: str = Field(max_length=255)

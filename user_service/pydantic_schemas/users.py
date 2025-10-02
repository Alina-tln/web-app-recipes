from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserSchema(BaseSchema):
    username: str = Field(max_length=100)
    email: EmailStr
    password_hash: str = Field(max_length=255)
    oauth_id: str | None = Field(max_length=255)
    provider_name: str | None = Field(max_length=100)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
from db_base import Base
from .groups import UserGroup
from sqlalchemy import Column, BigInteger, TIMESTAMP, func, String, Boolean, text, UniqueConstraint

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint("oauth_id", "provider_name", name="uq_user_oauth"),
        {"schema": "users"}
    )
    id = Column(BigInteger, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    oauth_id = Column(String(255), nullable=True)
    provider_name = Column(String(255))
    is_verified = Column(Boolean, server_default=text("false"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships to Recipe Service
    recipes = relationship("Recipe", back_populates="author")
    user_recipes = relationship("UserRecipe", back_populates="user")

    # Relationships for UserGroups
    groups = relationship("Group", secondary=UserGroup.__table__, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

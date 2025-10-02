from db_base import Base
from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

class UserGroup(Base):
    __tablename__ = 'user_groups'
    __table_args__ = {"schema": "users"}
    user_id = Column(BigInteger, ForeignKey('users.users.id', ondelete='CASCADE'), primary_key=True)
    group_id = Column(BigInteger, ForeignKey('users.groups.id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<UserGroup(user_id={self.user_id}, group_id={self.group_id})>"

class Group(Base):
    __tablename__ = 'groups'
    __table_args__ = {"schema": "users"}

    id = Column(BigInteger, primary_key=True)
    group_name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))

    users = relationship("User", secondary=UserGroup.__table__, back_populates="groups")

    def __repr__(self):
        return f"<Group(id={self.id}, group_name='{self.group_name}')>"





from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class UserRole(Enum):
    admin = 1
    viewer = 2


class Role(SQLModel, table=True):
    __tablename__ = 'roles'

    id: int | None = Field(default=None, primary_key=True)
    name: UserRole


class _UserSchema(BaseModel):
    username: str
    email: str
    full_name: str | None = None


class UserPublic(_UserSchema):
    role: UserRole = UserRole.viewer

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.admin

    @property
    def is_viewer(self) -> bool:
        return self.role == UserRole.viewer


class User(SQLModel, _UserSchema, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    role_id: int = Field(default=2, foreign_key="roles.id")

    def to_user_public(self) -> UserPublic:
        return UserPublic(
            username=self.username,
            email=self.email,
            full_name=self.full_name,
            role=UserRole(self.role_id)
        )


class UserCreate(_UserSchema):
    plain_password: str

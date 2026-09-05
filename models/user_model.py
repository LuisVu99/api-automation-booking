"""Pydantic models for user API payloads."""

from pydantic import BaseModel, ConfigDict, Field


class UserModel(BaseModel):
    """User representation returned by the API."""

    model_config = ConfigDict(extra="ignore")

    id: int | None = None
    name: str
    username: str
    email: str
    phone: str | None = None
    website: str | None = None


class UserCreateModel(BaseModel):
    """User payload accepted by the create-user endpoint."""

    name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    email: str = Field(min_length=3)

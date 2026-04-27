from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi_users import schemas
import uuid


class PostCreate(BaseModel):
    caption: str = Field(default="", max_length=500)

    @field_validator("caption")
    @classmethod
    def normalize_caption(cls, value: str) -> str:
        # Normalize whitespace so empty/space-only captions are stored consistently.
        return " ".join(value.split())

class PostResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    caption: str
    url: str
    file_type: Literal["image", "video"]
    file_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UploadResponse(BaseModel):
    post: PostResponse


class FeedPostResponse(PostResponse):
    is_owner: bool
    email: str


class FeedResponse(BaseModel):
    posts: list[FeedPostResponse]


class DeleteResponse(BaseModel):
    success: bool
    message: str

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
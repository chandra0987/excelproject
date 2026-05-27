from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UserModel(BaseModel):
    """Pydantic model representing a user document in MongoDB."""

    id: Optional[str] = Field(default=None, alias="_id")
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=255)
    hashed_password: str = Field(..., max_length=255)
    is_active: bool = True
    created_at: datetime = Field(default_factory=utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data: dict) -> "UserModel":
        """Convert a MongoDB document dict to a UserModel instance."""
        if data is None:
            return None
        data["_id"] = str(data["_id"])
        return cls(**data)

    def to_mongo(self) -> dict:
        """Convert to a MongoDB-compatible dict (exclude id for inserts)."""
        data = self.model_dump(by_alias=True, exclude={"id"})
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

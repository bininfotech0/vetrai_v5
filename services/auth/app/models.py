from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password_hash: str
    name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RefreshToken(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    token_hash: str  # store hashed refresh token
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class AccessToken(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    token_hash: str  # store hashed access token
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

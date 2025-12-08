import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select, SQLModel

from .models import User
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    store_refresh_token,
    verify_refresh_token,
    revoke_refresh_tokens_for_user,
    revoke_access_tokens_for_user,
    verify_access_token,
    engine as auth_engine,
)

# App and DB
app = FastAPI(title="VetrAI Auth Service")

# Reuse engine from auth module
engine = auth_engine

# Schemas
class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


@app.on_event("startup")
def on_startup():
    # ensure tables exist
    SQLModel.metadata.create_all(engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}


@app.post("/register", response_model=dict, status_code=201)
def register(payload: RegisterIn):
    with Session(engine) as session:
        q = select(User).where(User.email == payload.email)
        existing = session.exec(q).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(email=payload.email, password_hash=get_password_hash(payload.password), name=payload.name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "email": user.email, "name": user.name}


@app.post("/login", response_model=TokenOut)
def login(payload: LoginIn):
    with Session(engine) as session:
        q = select(User).where(User.email == payload.email)
        user = session.exec(q).first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # create opaque access token and refresh token
        access = create_access_token(session, user.id)
        refresh = create_refresh_token()
        expires_at = datetime.utcnow() + timedelta(seconds=int(os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", "2592000")))
        # store hashed refresh token
        store_refresh_token(session, user.id, refresh, expires_at=expires_at)
        return TokenOut(access_token=access, refresh_token=refresh)


class RefreshIn(BaseModel):
    user_id: str
    refresh_token: str


@app.post("/refresh", response_model=TokenOut)
def refresh(payload: RefreshIn):
    with Session(engine) as session:
        if not verify_refresh_token(session, payload.user_id, payload.refresh_token):
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # revoke existing refresh tokens and access tokens (rotation)
        revoke_refresh_tokens_for_user(session, payload.user_id)
        revoke_access_tokens_for_user(session, payload.user_id)
        # issue new tokens
        access = create_access_token(session, payload.user_id)
        refresh = create_refresh_token()
        expires_at = datetime.utcnow() + timedelta(seconds=int(os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", "2592000")))
        store_refresh_token(session, payload.user_id, refresh, expires_at=expires_at)
        return TokenOut(access_token=access, refresh_token=refresh)


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    with Session(engine) as session:
        user_id = verify_access_token(session, token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")
        q = select(User).where(User.id == user_id)
        user = session.exec(q).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user


@app.get("/users/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name}

import os
import hashlib
import time
import secrets
from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import Session, select, create_engine

from .models import User, RefreshToken, AccessToken

from passlib.hash import argon2

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vetrai_auth.db")
ACCESS_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "900"))
REFRESH_EXPIRE = int(os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", "2592000"))

# create engine (sqlite connect_args handled)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)


def get_password_hash(password: str) -> str:
    return argon2.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return argon2.verify(password, password_hash)
    except Exception:
        return False


# ---------- Refresh token helpers (unchanged, opaque tokens) ----------
def create_refresh_token() -> str:
    token = hashlib.sha256(str(time.time()).encode("utf-8") + os.urandom(16)).hexdigest()
    return token


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def store_refresh_token(session: Session, user_id: str, token: str, expires_at: Optional[datetime] = None):
    token_hash = hash_refresh_token(token)
    rt = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    session.add(rt)
    session.commit()
    session.refresh(rt)
    return rt


def revoke_refresh_tokens_for_user(session: Session, user_id: str):
    q = select(RefreshToken).where(RefreshToken.user_id == user_id)
    rts = session.exec(q).all()
    for rt in rts:
        session.delete(rt)
    session.commit()


def verify_refresh_token(session: Session, user_id: str, token: str) -> bool:
    token_hash = hash_refresh_token(token)
    q = select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.token_hash == token_hash)
    rt = session.exec(q).first()
    if not rt:
        return False
    if rt.expires_at and rt.expires_at < datetime.utcnow():
        # expired
        session.delete(rt)
        session.commit()
        return False
    return True


# ---------- Access token helpers (new, opaque tokens stored in DB) ----------
def _hash_token(token: str) -> str:
    # Central hashing for both access and refresh tokens
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(session: Session, user_id: str, expires_delta: Optional[int] = None) -> str:
    """
    Generate an opaque access token, store a hashed version in DB with expiry, and return the raw token.
    """
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expire_seconds = expires_delta if expires_delta is not None else ACCESS_EXPIRE
    expires_at = datetime.utcnow() + timedelta(seconds=expire_seconds)
    at = AccessToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    session.add(at)
    session.commit()
    session.refresh(at)
    return token


def verify_access_token(session: Session, token: str) -> Optional[str]:
    """
    Verify the provided opaque access token. Returns user_id if valid, otherwise None.
    """
    token_hash = _hash_token(token)
    q = select(AccessToken).where(AccessToken.token_hash == token_hash)
    at = session.exec(q).first()
    if not at:
        return None
    if at.expires_at and at.expires_at < datetime.utcnow():
        # expired - delete and return None
        session.delete(at)
        session.commit()
        return None
    return at.user_id


def revoke_access_tokens_for_user(session: Session, user_id: str):
    q = select(AccessToken).where(AccessToken.user_id == user_id)
    ats = session.exec(q).all()
    for at in ats:
        session.delete(at)
    session.commit()


def revoke_access_token_by_hash(session: Session, token_hash: str):
    q = select(AccessToken).where(AccessToken.token_hash == token_hash)
    at = session.exec(q).first()
    if at:
        session.delete(at)
        session.commit()


def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    q = select(User).where(User.id == user_id)
    return session.exec(q).first()

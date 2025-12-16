# FILE: app/core/security.py
# ============================================================================
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status

from app.core.config import settings


def _prehash_password(password: str) -> str:
    """Pre-hash password with SHA256 to avoid bcrypt's 72-byte limit.
    
    This is a secure approach that:
    1. Ensures passwords of any length can be hashed
    2. Always produces a fixed-length input for bcrypt (64 hex chars)
    3. Maintains security as SHA256 is cryptographically secure
    """
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    
    # Hash with SHA256 and return hex digest
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash.
    
    Pre-hashes the password with SHA256 before bcrypt verification.
    """
    # Pre-hash the password to avoid bcrypt's 72-byte limit
    prehashed = _prehash_password(plain_password)
    
    # Convert to bytes for bcrypt
    password_bytes = prehashed.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hash_bytes)


def get_password_hash(password: str) -> str:
    """Hash a password using SHA256 + bcrypt.
    
    Pre-hashes with SHA256 to avoid bcrypt's 72-byte limit,
    then applies bcrypt for secure password storage.
    """
    # Pre-hash the password to avoid bcrypt's 72-byte limit
    prehashed = _prehash_password(password)
    
    # Generate salt and hash with bcrypt
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(prehashed.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_password_strength(password: str) -> bool:
    """Validate password meets security requirements."""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

"""
Semptify55 Security Module
JWT handling and encryption utilities.
"""

import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from cryptography.fernet import Fernet
from passlib.context import CryptContext

from app.config import get_settings

# Password hashing (for future admin features)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_fernet_key() -> bytes:
    """Get or generate Fernet key from settings."""
    settings = get_settings()
    # Use secret_key to derive Fernet key (32 bytes required)
    import base64
    key = base64.urlsafe_b64encode(settings.secret_key[:32].encode().ljust(32, b'0'))
    return key


def encrypt_data(data: str) -> str:
    """Encrypt string data using Fernet."""
    f = Fernet(get_fernet_key())
    return f.encrypt(data.encode()).decode()


def decrypt_data(encrypted: str) -> str:
    """Decrypt Fernet-encrypted string."""
    f = Fernet(get_fernet_key())
    return f.decrypt(encrypted.encode()).decode()


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    settings = get_settings()
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "jti": uuid.uuid4().hex})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate JWT token."""
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_session_id() -> str:
    """Generate secure random session ID."""
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

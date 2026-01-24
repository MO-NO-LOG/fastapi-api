import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from jose import jwt

from app.config import settings

# Secret key for JWT (should be in env var, but hardcoded for now)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def generate_salt() -> str:
    """
    Generate a new random salt for password hashing.
    Returns the salt as a string.
    """
    return bcrypt.gensalt(rounds=12).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """
    Verify a plain password against a hashed password using the provided salt.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password from database
        salt: The salt from user_salt table

    Returns:
        True if password matches, False otherwise
    """
    computed_hash = bcrypt.hashpw(
        plain_password.encode("utf-8"), salt.encode("utf-8")
    ).decode("utf-8")
    return computed_hash == hashed_password


def get_password_hash(password: str, salt: str) -> str:
    """
    Hash a password using the provided salt.

    Args:
        password: The plain text password
        salt: The salt string (from generate_salt() or database)

    Returns:
        The hashed password as a string
    """
    return bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8")).decode("utf-8")


def create_password_hash_and_salt(password: str) -> Tuple[str, str]:
    """
    Generate both a salt and hash for a new password.

    Args:
        password: The plain text password

    Returns:
        Tuple of (hashed_password, salt)
    """
    salt = generate_salt()
    hashed = get_password_hash(password, salt)
    return hashed, salt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

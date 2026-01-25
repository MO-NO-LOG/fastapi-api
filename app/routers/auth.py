from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenResponse,
    RefreshTokenRequest,
)
from app.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.dependencies import get_current_user
from app.services.token_service import TokenBlacklistService, RefreshTokenService
from jose import JWTError
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_nickname = db.query(User).filter(User.nickname == user.nickname).first()
    if db_nickname:
        raise HTTPException(status_code=400, detail="Nickname already taken")

    # Hash password (bcrypt includes salt automatically)
    hashed_pw = get_password_hash(user.password)

    # Create user
    new_user = User(
        email=user.email,
        password=hashed_pw,
        name=user.name,
        nickname=user.nickname,
        gender=user.gender,
        bio=user.bio,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(response: Response, user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Verify password (bcrypt hash includes salt)
    if not verify_password(user_in.password, str(user.password)):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Set token expiration based on remember_me
    # If remember_me is True, token lasts 7 days; otherwise 30 minutes
    token_expires = timedelta(days=7) if user_in.remember_me else timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.email)}, expires_delta=token_expires
    )

    # Create refresh token (always valid for 7 days)
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": str(user.email)}, expires_delta=refresh_token_expires
    )

    # Store refresh token in Redis (async)
    await RefreshTokenService.store_refresh_token(
        email=str(user.email),
        refresh_token=refresh_token,
        expires_delta=refresh_token_expires,
    )

    # Set cookie duration to match token expiration
    cookie_max_age = 7 * 24 * 60 * 60 if user_in.remember_me else 30 * 60

    # Set access token cookie (store token without Bearer prefix in cookie)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=cookie_max_age,
        path="/",  # Cookie available for all paths
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )

    # Set refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        path="/",
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(
    response: Response,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    # Get access token from cookie or header
    access_token = request.cookies.get("access_token")
    if not access_token:
        # Try to get from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header[7:]

    # Add access token to blacklist (async)
    if access_token:
        await TokenBlacklistService.add_to_blacklist(access_token)

    # Delete refresh token from Redis (async)
    await RefreshTokenService.delete_refresh_token(str(current_user.email))

    # Delete cookies
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")

    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    response: Response, request: Request, db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.

    The refresh token can be provided either:
    1. In the request body
    2. In the refresh_token cookie
    """
    # Get refresh token from cookie or request body
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=401, detail="Refresh token not found in cookies"
        )

    try:
        # Decode refresh token
        payload = decode_token(refresh_token)
        email = payload.get("sub")
        token_type = payload.get("type")

        if not email or not isinstance(email, str) or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Verify refresh token against stored token in Redis (async)
        if not await RefreshTokenService.verify_refresh_token(email, refresh_token):
            raise HTTPException(
                status_code=401,
                detail="Refresh token is invalid or has been revoked",
            )

        # Get user from database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Create new access token
        access_token = create_access_token(
            data={"sub": str(user.email)}, expires_delta=timedelta(minutes=30)
        )

        # Create new refresh token
        new_refresh_token = create_refresh_token(
            data={"sub": str(user.email)}, expires_delta=timedelta(days=7)
        )

        # Update refresh token in Redis (async)
        await RefreshTokenService.store_refresh_token(
            email=str(user.email),
            refresh_token=new_refresh_token,
            expires_delta=timedelta(days=7),
        )

        # Set new access token cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=30 * 60,  # 30 minutes
            path="/",
            samesite="lax",
            secure=False,  # Set to True in production with HTTPS
        )

        # Set new refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            max_age=7 * 24 * 60 * 60,  # 7 days
            path="/",
            samesite="lax",
            secure=False,  # Set to True in production with HTTPS
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

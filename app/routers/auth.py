from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserSalt
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.utils import (
    verify_password,
    create_password_hash_and_salt,
    create_access_token,
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Generate hash and salt separately
    hashed_pw, salt = create_password_hash_and_salt(user.password)

    # Create user
    new_user = User(
        email=user.email,
        password=hashed_pw,
        name=user.nickname,
        dec=user.name,  # Store real name in dec if provided
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Store salt in separate table
    user_salt = UserSalt(uid=new_user.uid, salt=salt)
    db.add(user_salt)
    db.commit()

    return new_user


@router.post("/login", response_model=Token)
def login(response: Response, user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Retrieve salt from separate table
    user_salt = db.query(UserSalt).filter(UserSalt.uid == user.uid).first()
    if not user_salt:
        raise HTTPException(status_code=500, detail="User salt not found")

    # Verify password with salt
    if not verify_password(user_in.password, str(user.password), str(user_salt.salt)):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Set token expiration based on remember_me
    # If remember_me is True, token lasts 7 days; otherwise 30 minutes
    from datetime import timedelta

    token_expires = timedelta(days=7) if user_in.remember_me else timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=token_expires
    )

    # Set cookie duration to match token expiration
    cookie_max_age = 7 * 24 * 60 * 60 if user_in.remember_me else 30 * 60

    # Set cookie (store token without Bearer prefix in cookie)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=cookie_max_age,
        path="/",  # Cookie available for all paths
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(response: Response):
    # httpOnly 쿠키 삭제 (set_cookie와 동일한 path 설정 필요)
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Successfully logged out"}

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    nickname: str
    name: str
    gender: Optional[str] = None
    bio: Optional[str] = None


class UserLogin(UserBase):
    password: str
    remember_me: bool = False


class UserResponse(UserBase):
    uid: int
    name: str
    nickname: str
    img: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# Movie Schemas
class MovieResponseItem(BaseModel):
    id: int
    title: str
    posterUrl: Optional[str] = None
    genres: List[str] = []
    averageRating: float
    releaseDate: Optional[date] = None


class MovieDetailResponse(MovieResponseItem):
    description: Optional[str] = None


class MovieDetailRequest(BaseModel):
    movieId: int


# Search Schemas
class MovieSearchRequest(BaseModel):
    keyword: str = ""
    searchType: str = "TITLE"  # TITLE, DIRECTOR, GENRE


class MovieSearchResponse(BaseModel):
    movies: List[MovieResponseItem]
    totalPages: int


# Review Schemas
class ReviewCreateRequest(BaseModel):
    movieId: int
    content: str
    rating: float


class ReviewResponseItem(BaseModel):
    userId: int
    userNickname: str
    rating: float
    content: str
    createdAt: datetime


class ReviewListResponse(BaseModel):
    reviews: List[ReviewResponseItem]


class ReviewListRequest(BaseModel):
    movieId: int


# User Detail Schemas
class UserDetailReviewItem(BaseModel):
    reviewId: int
    movieId: int
    movieTitle: str
    rating: Optional[float] = None
    content: str
    createdAt: datetime


class UserDetailResponse(BaseModel):
    userId: int
    nickname: str
    email: str
    profileImage: Optional[str] = None
    bio: Optional[str] = None
    reviewCount: int
    commentCount: int
    joinedAt: datetime
    reviews: List[UserDetailReviewItem] = []


# Auth Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str

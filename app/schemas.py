from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    nickname: str
    name: Optional[str] = None


class UserLogin(UserBase):
    password: str
    remember_me: bool = False


class UserResponse(UserBase):
    uid: int
    name: str
    img: Optional[str] = None
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


# Auth Token
class Token(BaseModel):
    access_token: str
    token_type: str

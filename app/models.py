from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Numeric,
    CHAR,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    nickname = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    img = Column(String(255), default="default")
    bio = Column(Text, nullable=True)
    gender = Column(
        CHAR(1), nullable=True
    )
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship("Review", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Movie(Base):
    __tablename__ = "movie"

    mid = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    dec = Column(Text, nullable=True)
    rat = Column(Numeric(2, 1), default=0)
    release_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    director = Column(String(100), nullable=True)  # Added director
    poster_url = Column(String(255), nullable=True)  # Added for UI

    genres = relationship("MovieGenre", back_populates="movie")
    reviews = relationship("Review", back_populates="movie")


class Genre(Base):
    __tablename__ = "genre"

    gid = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    movies = relationship("MovieGenre", back_populates="genre")


class MovieGenre(Base):
    __tablename__ = "movie_genre"

    mid = Column(Integer, ForeignKey("movie.mid", ondelete="CASCADE"), primary_key=True)
    gid = Column(Integer, ForeignKey("genre.gid", ondelete="CASCADE"), primary_key=True)

    movie = relationship("Movie", back_populates="genres")
    genre = relationship("Genre", back_populates="movies")


class Review(Base):
    __tablename__ = "review"

    rid = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    mid = Column(Integer, ForeignKey("movie.mid", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=True)
    dec = Column(Text, nullable=False)
    rat = Column(Numeric(2, 1), nullable=True)  # Check 1-5
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
    comments = relationship("Comment", back_populates="review")
    likes = relationship("ReviewLike", back_populates="review")


class Comment(Base):
    __tablename__ = "comment"

    cid = Column(Integer, primary_key=True, index=True)
    rid = Column(Integer, ForeignKey("review.rid", ondelete="CASCADE"), nullable=False)
    uid = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    dec = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review = relationship("Review", back_populates="comments")
    user = relationship("User", back_populates="comments")
    likes = relationship("CommentLike", back_populates="comment")


class ReviewLike(Base):
    __tablename__ = "review_like"

    lid = Column(Integer, primary_key=True, index=True)
    rid = Column(Integer, ForeignKey("review.rid", ondelete="CASCADE"), nullable=False)
    uid = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    type = Column(CHAR(1), nullable=True)  # L or D
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review = relationship("Review", back_populates="likes")


class CommentLike(Base):
    __tablename__ = "comment_like"

    lid = Column(Integer, primary_key=True, index=True)
    cid = Column(Integer, ForeignKey("comment.cid", ondelete="CASCADE"), nullable=False)
    uid = Column(Integer, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    type = Column(CHAR(1), nullable=True)  # L or D
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    comment = relationship("Comment", back_populates="likes")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.models import Movie, MovieGenre, Genre
from app.schemas import (
    MovieResponseItem,
    MovieDetailResponse,
    MovieDetailRequest,
    MovieSearchResponse,
    MovieSearchRequest,
)
from typing import List

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.post("/search", response_model=MovieSearchResponse)
def search_movies(
    params: MovieSearchRequest,
    page: int = 0,
    size: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Movie)

    if params.keyword:
        if params.searchType == "TITLE":
            query = query.filter(Movie.title.ilike(f"%{params.keyword}%"))
        elif params.searchType == "DIRECTOR":
            query = query.filter(Movie.director.ilike(f"%{params.keyword}%"))
        elif params.searchType == "GENRE":
            query = (
                query.join(MovieGenre)
                .join(Genre)
                .filter(Genre.name.ilike(f"%{params.keyword}%"))
            )

    total_count = query.count()
    movies = query.offset(page * size).limit(size).all()

    total_pages = (total_count + size - 1) // size

    result = []
    for m in movies:
        genres = [g.genre.name for g in m.genres]
        result.append(
            MovieResponseItem(
                id=m.mid,
                title=m.title,
                posterUrl=m.poster_url,
                genres=genres,
                averageRating=float(m.rat) if m.rat else 0.0,
                releaseDate=m.release_date,
            )
        )

    return {"movies": result, "totalPages": total_pages}


@router.get("/trend", response_model=List[MovieResponseItem])
def get_trend_movies(db: Session = Depends(get_db)):
    # Top 10 by rating
    movies = db.query(Movie).order_by(desc(Movie.rat)).limit(10).all()

    result = []
    for m in movies:
        genres = [g.genre.name for g in m.genres]
        result.append(
            MovieResponseItem(
                id=m.mid,
                title=m.title,
                posterUrl=m.poster_url,
                genres=genres,
                averageRating=float(m.rat) if m.rat else 0.0,
                releaseDate=m.release_date,
            )
        )
    return result


@router.post("/detail", response_model=MovieDetailResponse)
def get_movie_detail(req: MovieDetailRequest, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.mid == req.movieId).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    genres = [g.genre.name for g in movie.genres]

    return MovieDetailResponse(
        id=movie.mid,
        title=movie.title,
        posterUrl=movie.poster_url,
        genres=genres,
        averageRating=float(movie.rat) if movie.rat else 0.0,
        releaseDate=movie.release_date,
        description=movie.dec,
    )


@router.get("/recommended", response_model=List[MovieResponseItem])
def get_recommended_movies(limit: int = 4, db: Session = Depends(get_db)):
    # Random movies with rating >= 3
    # SQLAlchemy random is tricky across DBs, usually func.random() for PG
    movies = (
        db.query(Movie)
        .filter(Movie.rat >= 3.0)
        .order_by(func.random())
        .limit(limit)
        .all()
    )

    # If not enough rated movies, just random movies
    if len(movies) < limit:
        movies = db.query(Movie).order_by(func.random()).limit(limit).all()

    result = []
    for m in movies:
        genres = [g.genre.name for g in m.genres]
        result.append(
            MovieResponseItem(
                id=m.mid,
                title=m.title,
                posterUrl=m.poster_url,
                genres=genres,
                averageRating=float(m.rat) if m.rat else 0.0,
                releaseDate=m.release_date,
            )
        )
    return result

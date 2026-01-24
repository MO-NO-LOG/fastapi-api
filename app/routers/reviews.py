from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Review, User
from app.schemas import (
    ReviewListResponse,
    ReviewListRequest,
    ReviewResponseItem,
    ReviewCreateRequest,
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/by-movie", response_model=ReviewListResponse)
def get_reviews_by_movie(req: ReviewListRequest, db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.mid == req.movieId)
        .order_by(desc(Review.created_at))
        .all()
    )

    result = []
    for r in reviews:
        # Fetch user nickname (r.user.name)
        # Note: r.user might load lazily.
        # If user is None (shouldn't happen with FK constraint), handle gracefully.
        nickname = r.user.name if r.user else "Unknown"

        result.append(
            ReviewResponseItem(
                userId=r.uid,
                userNickname=nickname,
                rating=float(r.rat),
                content=r.dec,
                createdAt=r.created_at,
            )
        )

    return {"reviews": result}


@router.post("/create")
def create_review(
    req: ReviewCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if already reviewed
    existing = (
        db.query(Review)
        .filter(Review.uid == current_user.uid, Review.mid == req.movieId)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="You have already reviewed this movie."
        )

    new_review = Review(
        uid=current_user.uid, mid=req.movieId, dec=req.content, rat=req.rating
    )
    db.add(new_review)
    db.commit()

    return {"message": "Review created successfully"}

"""
DB에 예시 데이터를 추가하는 스크립트

Usage:
    uv run python scripts/seed_data.py
"""

import sys
import os
from datetime import date

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    User,
    Movie,
    Genre,
    MovieGenre,
    Review,
    Comment,
    ReviewLike,
    CommentLike,
)
from app.utils import get_password_hash


def seed_users(db: Session):
    """사용자 예시 데이터 추가"""
    print("Adding sample users...")

    users_data = [
        {
            "name": "관리자",
            "nickname": "admin",
            "email": "admin@mono-log.com",
            "password": get_password_hash("admin1234"),
            "img": "/images/admin.png",
            "bio": "MO-NO-LOG 관리자입니다.",
            "gender": "M",
            "is_admin": True,
        },
        {
            "name": "김영화",
            "nickname": "movie_lover",
            "email": "kim@example.com",
            "password": get_password_hash("password123"),
            "img": "/images/user1.png",
            "bio": "영화를 사랑하는 평범한 직장인입니다.",
            "gender": "F",
            "is_admin": False,
        },
        {
            "name": "박리뷰",
            "nickname": "reviewer_park",
            "email": "park@example.com",
            "password": get_password_hash("password123"),
            "img": "/images/user2.png",
            "bio": "주말마다 영화관을 찾는 영화 매니아입니다.",
            "gender": "M",
            "is_admin": False,
        },
        {
            "name": "이시네마",
            "nickname": "cinema_lee",
            "email": "lee@example.com",
            "password": get_password_hash("password123"),
            "img": "/images/user3.png",
            "bio": "고전 영화부터 최신작까지 두루 섭렵합니다.",
            "gender": "F",
            "is_admin": False,
        },
        {
            "name": "최영상",
            "nickname": "film_choi",
            "email": "choi@example.com",
            "password": get_password_hash("password123"),
            "img": "/images/user4.png",
            "bio": "영화 제작 공부 중인 학생입니다.",
            "gender": "M",
            "is_admin": False,
        },
    ]

    users = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        users.append(user)

    db.commit()
    print(f"✓ Added {len(users)} users")
    return users


def seed_genres(db: Session):
    """장르 예시 데이터 추가"""
    print("Adding sample genres...")

    genre_names = [
        "액션",
        "코미디",
        "드라마",
        "SF",
        "스릴러",
        "공포",
        "로맨스",
        "애니메이션",
        "판타지",
        "미스터리",
        "범죄",
        "모험",
        "다큐멘터리",
        "전쟁",
        "뮤지컬",
    ]

    genres = []
    for name in genre_names:
        genre = Genre(name=name)
        db.add(genre)
        genres.append(genre)

    db.commit()
    print(f"✓ Added {len(genres)} genres")
    return genres


def seed_movies(db: Session, genres: list):
    """영화 예시 데이터 추가"""
    print("Adding sample movies...")

    movies_data = [
        {
            "title": "인셉션",
            "dec": "꿈 속의 꿈을 통해 타인의 잠재의식에 침투하는 특수 요원들의 이야기",
            "rat": 4.5,
            "release_date": date(2010, 7, 21),
            "director": "크리스토퍼 놀란",
            "poster_url": "/images/inception.jpg",
            "genre_names": ["SF", "액션", "스릴러"],
        },
        {
            "title": "기생충",
            "dec": "전원 백수인 기택 가족이 부유한 박 사장 가족에게 기생하며 벌어지는 이야기",
            "rat": 4.8,
            "release_date": date(2019, 5, 30),
            "director": "봉준호",
            "poster_url": "/images/parasite.jpg",
            "genre_names": ["드라마", "스릴러", "코미디"],
        },
        {
            "title": "인터스텔라",
            "dec": "황폐해진 지구를 떠나 인류의 새로운 보금자리를 찾는 우주 탐사대의 모험",
            "rat": 4.6,
            "release_date": date(2014, 11, 6),
            "director": "크리스토퍼 놀란",
            "poster_url": "/images/interstellar.jpg",
            "genre_names": ["SF", "모험", "드라마"],
        },
        {
            "title": "라라랜드",
            "dec": "재즈 피아니스트와 배우 지망생이 꿈을 좇으며 사랑에 빠지는 이야기",
            "rat": 4.3,
            "release_date": date(2016, 12, 7),
            "director": "데이미언 셔젤",
            "poster_url": "/images/lalaland.jpg",
            "genre_names": ["로맨스", "뮤지컬", "드라마"],
        },
        {
            "title": "어벤져스: 엔드게임",
            "dec": "타노스에게 패배한 어벤져스가 다시 모여 최후의 반격을 시도하는 이야기",
            "rat": 4.4,
            "release_date": date(2019, 4, 24),
            "director": "앤서니 루소, 조 루소",
            "poster_url": "/images/endgame.jpg",
            "genre_names": ["액션", "SF", "모험"],
        },
        {
            "title": "조커",
            "dec": "코미디언을 꿈꾸던 한 남자가 광기 어린 악당 조커로 변해가는 과정",
            "rat": 4.2,
            "release_date": date(2019, 10, 2),
            "director": "토드 필립스",
            "poster_url": "/images/joker.jpg",
            "genre_names": ["드라마", "스릴러", "범죄"],
        },
        {
            "title": "센과 치히로의 행방불명",
            "dec": "신들의 세계로 들어간 소녀 치히로가 부모를 구하기 위해 고군분투하는 판타지 애니메이션",
            "rat": 4.7,
            "release_date": date(2001, 7, 20),
            "director": "미야자키 하야오",
            "poster_url": "/images/spirited_away.jpg",
            "genre_names": ["애니메이션", "판타지", "모험"],
        },
        {
            "title": "다크 나이트",
            "dec": "배트맨과 조커의 대결을 그린 배트맨 시리즈의 두 번째 작품",
            "rat": 4.6,
            "release_date": date(2008, 7, 18),
            "director": "크리스토퍼 놀란",
            "poster_url": "/images/dark_knight.jpg",
            "genre_names": ["액션", "범죄", "드라마"],
        },
        {
            "title": "쇼생크 탈출",
            "dec": "억울하게 누명을 쓴 은행가가 교도소에서 희망을 잃지 않고 탈출을 준비하는 이야기",
            "rat": 4.9,
            "release_date": date(1994, 9, 23),
            "director": "프랭크 다라본트",
            "poster_url": "/images/shawshank.jpg",
            "genre_names": ["드라마"],
        },
        {
            "title": "펄프 픽션",
            "dec": "로스앤젤레스의 범죄자들의 얽히고설킨 이야기를 독특한 구성으로 풀어낸 작품",
            "rat": 4.4,
            "release_date": date(1994, 10, 14),
            "director": "퀜틴 타란티노",
            "poster_url": "/images/pulp_fiction.jpg",
            "genre_names": ["범죄", "드라마"],
        },
    ]

    # 장르 이름으로 장르 객체를 찾기 위한 딕셔너리
    genre_dict = {g.name: g for g in genres}

    movies = []
    for movie_data in movies_data:
        genre_names = movie_data.pop("genre_names")
        movie = Movie(**movie_data)
        db.add(movie)
        db.flush()  # mid를 얻기 위해 flush

        # 영화-장르 관계 추가
        for genre_name in genre_names:
            if genre_name in genre_dict:
                movie_genre = MovieGenre(mid=movie.mid, gid=genre_dict[genre_name].gid)
                db.add(movie_genre)

        movies.append(movie)

    db.commit()
    print(f"✓ Added {len(movies)} movies")
    return movies


def seed_reviews(db: Session, users: list, movies: list):
    """리뷰 예시 데이터 추가"""
    print("Adding sample reviews...")

    reviews_data = [
        {
            "user_idx": 1,  # movie_lover
            "movie_idx": 0,  # 인셉션
            "title": "꿈과 현실의 경계를 허무는 걸작",
            "dec": "크리스토퍼 놀란의 상상력이 빛나는 작품입니다. 복잡한 구조임에도 불구하고 긴장감을 유지하며 관객을 끝까지 몰입시킵니다. 영상미와 음악, 연기 모든 면에서 완성도가 높습니다.",
            "rat": 5.0,
        },
        {
            "user_idx": 2,  # reviewer_park
            "movie_idx": 1,  # 기생충
            "title": "한국 영화의 자랑스러운 걸작",
            "dec": "계급 사회를 날카롭게 비판하면서도 재미를 잃지 않는 봉준호 감독의 연출이 돋보입니다. 배우들의 연기도 훌륭하고, 반전의 연속으로 긴장감이 넘칩니다.",
            "rat": 5.0,
        },
        {
            "user_idx": 3,  # cinema_lee
            "movie_idx": 2,  # 인터스텔라
            "title": "우주를 배경으로 한 감동적인 부녀애",
            "dec": "과학적 고증과 감성적인 스토리가 조화를 이루는 작품입니다. 우주의 광활함과 인간의 작은 사랑이 대비되면서 큰 감동을 선사합니다. 한스 짐머의 음악도 일품입니다.",
            "rat": 4.5,
        },
        {
            "user_idx": 1,  # movie_lover
            "movie_idx": 3,  # 라라랜드
            "title": "아름다운 음악과 영상의 향연",
            "dec": "재즈와 뮤지컬이 어우러진 화려한 영상미가 인상적입니다. 꿈을 좇는 두 사람의 이야기가 현실적이면서도 낭만적으로 그려집니다. 엔딩은 여운이 깊게 남습니다.",
            "rat": 4.0,
        },
        {
            "user_idx": 4,  # film_choi
            "movie_idx": 4,  # 어벤져스: 엔드게임
            "title": "마블 시네마틱 유니버스의 완벽한 피날레",
            "dec": "10년간 쌓아온 마블 영화들의 대단원입니다. 팬서비스가 넘치면서도 감동적인 순간들이 많아 만족스러웠습니다. 액션 장면도 화려하고 웅장합니다.",
            "rat": 4.5,
        },
        {
            "user_idx": 2,  # reviewer_park
            "movie_idx": 5,  # 조커
            "title": "호아킨 피닉스의 소름 돋는 연기",
            "dec": "악당의 기원을 다룬 작품 중 가장 인상적입니다. 호아킨 피닉스의 연기는 압도적이며, 사회의 어두운 면을 날카롭게 포착합니다. 불편하지만 강렬한 영화입니다.",
            "rat": 4.0,
        },
        {
            "user_idx": 3,  # cinema_lee
            "movie_idx": 6,  # 센과 치히로의 행방불명
            "title": "지브리의 최고 걸작",
            "dec": "어른이 되어 다시 봐도 감동적인 작품입니다. 아름다운 그림과 깊이 있는 스토리, 인상적인 캐릭터들이 어우러져 완벽한 애니메이션을 만들어냅니다.",
            "rat": 5.0,
        },
        {
            "user_idx": 4,  # film_choi
            "movie_idx": 7,  # 다크 나이트
            "title": "히어로 영화의 새로운 기준",
            "dec": "단순한 히어로물을 넘어 범죄 스릴러로서도 훌륭합니다. 히스 레저의 조커 연기는 전설적이며, 배트맨과의 대결 구도가 긴장감 넘칩니다.",
            "rat": 4.5,
        },
        {
            "user_idx": 1,  # movie_lover
            "movie_idx": 8,  # 쇼생크 탈출
            "title": "희망에 대한 영화",
            "dec": "절망적인 상황에서도 희망을 잃지 않는 주인공의 이야기가 가슴 깊이 와닿습니다. 완벽한 각본과 연기, 연출이 조화를 이룬 명작입니다.",
            "rat": 5.0,
        },
        {
            "user_idx": 2,  # reviewer_park
            "movie_idx": 9,  # 펄프 픽션
            "title": "타란티노의 천재성이 빛나는 작품",
            "dec": "비선형적 구조가 신선하고, 대사 하나하나가 인상적입니다. 폭력적이지만 유머러스하고, 독특한 매력이 가득한 영화입니다.",
            "rat": 4.5,
        },
        {
            "user_idx": 3,  # cinema_lee
            "movie_idx": 0,  # 인셉션
            "title": "몇 번을 봐도 새로운 영화",
            "dec": "볼 때마다 새로운 디테일을 발견하게 되는 영화입니다. 꿈의 층위를 넘나드는 구조가 복잡하지만 명확하게 전달됩니다.",
            "rat": 4.5,
        },
        {
            "user_idx": 4,  # film_choi
            "movie_idx": 1,  # 기생충
            "title": "영화 제작 관점에서도 배울 점이 많은 작품",
            "dec": "모든 장면이 의미를 가지고 있으며, 복선과 상징이 정교하게 배치되어 있습니다. 영화를 공부하는 입장에서 매우 유익한 작품입니다.",
            "rat": 5.0,
        },
    ]

    reviews = []
    for review_data in reviews_data:
        user_idx = review_data.pop("user_idx")
        movie_idx = review_data.pop("movie_idx")
        review = Review(
            uid=users[user_idx].uid, mid=movies[movie_idx].mid, **review_data
        )
        db.add(review)
        reviews.append(review)

    db.commit()
    print(f"✓ Added {len(reviews)} reviews")
    return reviews


def seed_comments(db: Session, users: list, reviews: list):
    """댓글 예시 데이터 추가"""
    print("Adding sample comments...")

    comments_data = [
        {
            "review_idx": 0,
            "user_idx": 2,
            "dec": "정말 공감되는 리뷰네요! 저도 이 영화 정말 좋아합니다.",
        },
        {
            "review_idx": 0,
            "user_idx": 3,
            "dec": "꿈의 층위를 설명하는 부분이 정말 인상적이었죠.",
        },
        {
            "review_idx": 1,
            "user_idx": 1,
            "dec": "기생충은 정말 볼 때마다 새로운 것 같아요.",
        },
        {
            "review_idx": 2,
            "user_idx": 4,
            "dec": "한스 짐머 음악 정말 최고죠! 영화와 완벽하게 어울립니다.",
        },
        {
            "review_idx": 3,
            "user_idx": 2,
            "dec": "엔딩 장면에서 정말 울었어요 ㅠㅠ",
        },
        {
            "review_idx": 4,
            "user_idx": 3,
            "dec": "아이언맨 팬으로서 너무 감동적이었습니다.",
        },
        {
            "review_idx": 5,
            "user_idx": 1,
            "dec": "호아킨 피닉스 연기 정말 소름 돋았어요.",
        },
        {
            "review_idx": 6,
            "user_idx": 2,
            "dec": "어렸을 때 봤던 기억이 나서 다시 봤는데 여전히 좋네요.",
        },
        {
            "review_idx": 7,
            "user_idx": 1,
            "dec": "히스 레저의 조커를 잊을 수가 없어요.",
        },
        {
            "review_idx": 8,
            "user_idx": 3,
            "dec": "이 영화는 정말 명작 중의 명작입니다.",
        },
    ]

    comments = []
    for comment_data in comments_data:
        review_idx = comment_data.pop("review_idx")
        user_idx = comment_data.pop("user_idx")
        comment = Comment(
            rid=reviews[review_idx].rid, uid=users[user_idx].uid, **comment_data
        )
        db.add(comment)
        comments.append(comment)

    db.commit()
    print(f"✓ Added {len(comments)} comments")
    return comments


def seed_likes(db: Session, users: list, reviews: list, comments: list):
    """좋아요 예시 데이터 추가"""
    print("Adding sample likes...")

    # 리뷰 좋아요
    review_likes_data = [
        {"review_idx": 0, "user_idx": 2, "type": "L"},
        {"review_idx": 0, "user_idx": 3, "type": "L"},
        {"review_idx": 0, "user_idx": 4, "type": "L"},
        {"review_idx": 1, "user_idx": 1, "type": "L"},
        {"review_idx": 1, "user_idx": 3, "type": "L"},
        {"review_idx": 2, "user_idx": 1, "type": "L"},
        {"review_idx": 2, "user_idx": 2, "type": "L"},
        {"review_idx": 3, "user_idx": 2, "type": "L"},
        {"review_idx": 4, "user_idx": 1, "type": "L"},
        {"review_idx": 5, "user_idx": 3, "type": "L"},
        {"review_idx": 6, "user_idx": 1, "type": "L"},
        {"review_idx": 6, "user_idx": 4, "type": "L"},
        {"review_idx": 7, "user_idx": 2, "type": "L"},
        {"review_idx": 8, "user_idx": 2, "type": "L"},
        {"review_idx": 8, "user_idx": 4, "type": "L"},
    ]

    review_likes = []
    for like_data in review_likes_data:
        review_idx = like_data.pop("review_idx")
        user_idx = like_data.pop("user_idx")
        like = ReviewLike(
            rid=reviews[review_idx].rid, uid=users[user_idx].uid, **like_data
        )
        db.add(like)
        review_likes.append(like)

    # 댓글 좋아요
    comment_likes_data = [
        {"comment_idx": 0, "user_idx": 1, "type": "L"},
        {"comment_idx": 1, "user_idx": 1, "type": "L"},
        {"comment_idx": 2, "user_idx": 2, "type": "L"},
        {"comment_idx": 3, "user_idx": 3, "type": "L"},
        {"comment_idx": 4, "user_idx": 1, "type": "L"},
        {"comment_idx": 5, "user_idx": 2, "type": "L"},
        {"comment_idx": 6, "user_idx": 2, "type": "L"},
        {"comment_idx": 7, "user_idx": 3, "type": "L"},
    ]

    comment_likes = []
    for like_data in comment_likes_data:
        comment_idx = like_data.pop("comment_idx")
        user_idx = like_data.pop("user_idx")
        like = CommentLike(
            cid=comments[comment_idx].cid, uid=users[user_idx].uid, **like_data
        )
        db.add(like)
        comment_likes.append(like)

    db.commit()
    print(
        f"✓ Added {len(review_likes)} review likes and {len(comment_likes)} comment likes"
    )


def seed_all():
    """모든 예시 데이터를 추가하는 메인 함수"""
    print("=" * 50)
    print("Starting to seed database with sample data...")
    print("=" * 50)

    db = SessionLocal()
    try:
        # 데이터 추가 순서: 의존성이 없는 것부터
        users = seed_users(db)
        genres = seed_genres(db)
        movies = seed_movies(db, genres)
        reviews = seed_reviews(db, users, movies)
        comments = seed_comments(db, users, reviews)
        seed_likes(db, users, reviews, comments)

        print("=" * 50)
        print("✅ Database seeding completed successfully!")
        print("=" * 50)
        print("\n샘플 로그인 정보:")
        print("  관리자: admin@mono-log.com / admin1234")
        print("  일반 사용자: kim@example.com / password123")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()

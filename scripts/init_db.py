import sys
import os
from sqlalchemy import create_engine, text

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import (
    DEFAULT_DATABASE_URL,
    SQLALCHEMY_DATABASE_URL,
)
from app.config import settings
from app.models import Base, User, UserSalt, Movie, Genre, MovieGenre, Review
from app.utils import create_password_hash_and_salt
from sqlalchemy.orm import sessionmaker
import datetime


def init_db():
    # 1. Create Database if not exists
    engine_default = create_engine(DEFAULT_DATABASE_URL, isolation_level="AUTOCOMMIT")
    with engine_default.connect() as conn:
        result = conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
        )
        if not result.scalar():
            print(f"Creating database {settings.DB_NAME}...")
            conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
        else:
            print(f"Database {settings.DB_NAME} already exists.")

    # 2. Connect to the new database
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # 3. Create Tables
    print("Creating tables...")
    Base.metadata.drop_all(bind=engine)  # Reset for clean state
    Base.metadata.create_all(bind=engine)

    # 4. Seed Data
    print("Seeding data...")

    # Users
    hashed_password1, salt1 = create_password_hash_and_salt("1234")
    user1 = User(
        name="admin",
        email="admin@test.com",
        password=hashed_password1,
        gender="M",
        birth_date=datetime.date(1990, 1, 1),
        is_admin=True,  # 관리자 계정
    )
    session.add(user1)
    session.flush()  # Get user1.uid

    # Store salt for user1
    user_salt1 = UserSalt(uid=user1.uid, salt=salt1)
    session.add(user_salt1)

    hashed_password2, salt2 = create_password_hash_and_salt("1234")
    user2 = User(
        name="jane",
        email="jane@test.com",
        password=hashed_password2,
        gender="F",
        birth_date=datetime.date(1995, 5, 5),
        is_admin=False,
    )
    session.add(user2)
    session.flush()  # Get user2.uid

    # Store salt for user2
    user_salt2 = UserSalt(uid=user2.uid, salt=salt2)
    session.add(user_salt2)

    session.commit()

    # Genres
    genres = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Crime",
        "Drama",
        "Fantasy",
        "Horror",
        "Mystery",
        "Romance",
        "Sci-Fi",
        "Thriller",
    ]
    genre_map = {}
    for g_name in genres:
        genre = Genre(name=g_name)
        session.add(genre)
        session.flush()
        genre_map[g_name] = genre

    # Movies (mapped to images found)
    movies_data = [
        {
            "title": "명탐정 피카츄",
            "img": "images/posters/1.명탐정 피카츄.webp",
            "genres": ["Animation", "Mystery"],
            "director": "Rob Letterman",
        },
        {
            "title": "나우 유 씨미",
            "img": "images/posters/2. 나우 유 씨미.webp",
            "genres": ["Crime", "Mystery"],
            "director": "Louis Leterrier",
        },
        {
            "title": "기묘한 이야기",
            "img": "images/posters/3. 기묘한 이야기.webp",
            "genres": ["Drama", "Fantasy"],
            "director": "Duffer Brothers",
        },
        {
            "title": "쇼생크 탈출",
            "img": "images/posters/4. 쇼생크 탈출.webp",
            "genres": ["Drama", "Crime"],
            "director": "Frank Darabont",
        },
        {
            "title": "센과 치히로의 행방불명",
            "img": "images/posters/5. 센과 치히로의 행방불명.webp",
            "genres": ["Animation", "Fantasy"],
            "director": "Hayao Miyazaki",
        },
        {
            "title": "너의 이름은",
            "img": "images/posters/6. 너의 이름은.webp",
            "genres": ["Animation", "Romance"],
            "director": "Makoto Shinkai",
        },
        {
            "title": "기생충",
            "img": "images/posters/7. 기생충.webp",
            "genres": ["Drama", "Thriller"],
            "director": "Bong Joon-ho",
        },
        {
            "title": "주토피아",
            "img": "images/posters/8. 주토피아.webp",
            "genres": ["Animation", "Adventure"],
            "director": "Byron Howard",
        },
        {
            "title": "타이타닉",
            "img": "images/posters/9. 타이타닉.webp",
            "genres": ["Romance", "Drama"],
            "director": "James Cameron",
        },
        {
            "title": "어벤져스: 엔드게임",
            "img": "images/posters/10. 어벤져스 엔드게임.webp",
            "genres": ["Action", "Sci-Fi"],
            "director": "Anthony Russo",
        },
        {
            "title": "캐리비안의 해적",
            "img": "images/posters/11. 캐리비안의 해저기 블랙펄의 저주.webp",
            "genres": ["Action", "Adventure"],
            "director": "Gore Verbinski",
        },
        {
            "title": "인셉션",
            "img": "images/posters/12. 인셉션.webp",
            "genres": ["Action", "Sci-Fi"],
            "director": "Christopher Nolan",
        },
        {
            "title": "인터스텔라",
            "img": "images/posters/13. 인터스텔라.webp",
            "genres": ["Sci-Fi", "Drama"],
            "director": "Christopher Nolan",
        },
        {
            "title": "터미네이터",
            "img": "images/posters/14. 터미네이터.webp",
            "genres": ["Action", "Sci-Fi"],
            "director": "James Cameron",
        },
        {
            "title": "트루먼 쇼",
            "img": "images/posters/15. 트루먼 쇼.webp",
            "genres": ["Comedy", "Drama"],
            "director": "Peter Weir",
        },
        {
            "title": "하울의 움직이는 성",
            "img": "images/posters/16. 하울의 움직이는 성.webp",
            "genres": ["Animation", "Fantasy"],
            "director": "Hayao Miyazaki",
        },
        {
            "title": "나타지마동강세",
            "img": "images/posters/17. 나타지마동강세.webp",
            "genres": ["Animation", "Fantasy"],
            "director": "Yu Yang",
        },
        {
            "title": "이웃집 토토로",
            "img": "images/posters/18. 이웃집 토토로.webp",
            "genres": ["Animation", "Fantasy"],
            "director": "Hayao Miyazaki",
        },
        {
            "title": "라따뚜이",
            "img": "images/posters/19. 라따뚜이.webp",
            "genres": ["Animation", "Comedy"],
            "director": "Brad Bird",
        },
        {
            "title": "드래곤 길들이기",
            "img": "images/posters/20. 드래곤 길들이기.webp",
            "genres": ["Animation", "Adventure"],
            "director": "Dean DeBlois",
        },
        {
            "title": "애나벨",
            "img": "images/posters/21. 애나벨.webp",
            "genres": ["Horror", "Mystery"],
            "director": "John R. Leonetti",
        },
        {
            "title": "곤지암",
            "img": "images/posters/22. 곤지암.webp",
            "genres": ["Horror"],
            "director": "Jung Bum-shik",
        },
        {
            "title": "그것 웰컴 투 데리",
            "img": "images/posters/23. 그것 웰컴 투 데리.webp",
            "genres": ["Horror"],
            "director": "Andy Muschietti",
        },
        {
            "title": "귀멸의 칼날",
            "img": "images/posters/24. 귀멸의칼날.webp",
            "genres": ["Animation", "Action"],
            "director": "Haruo Sotozaki",
        },
        {
            "title": "블랙팬서",
            "img": "images/posters/25. 블랙팬서.webp",
            "genres": ["Action", "Sci-Fi"],
            "director": "Ryan Coogler",
        },
        {
            "title": "나 홀로 집에",
            "img": "images/posters/26. 나 홀로 집에.webp",
            "genres": ["Comedy", "Family"],
            "director": "Chris Columbus",
        },
    ]

    for m_data in movies_data:
        movie = Movie(
            title=m_data["title"],
            poster_url=m_data["img"],
            director=m_data["director"],
            dec=f"This is a description for {m_data['title']}.",
            rat=0.0,
            release_date=datetime.date(2020, 1, 1),  # Dummy date
        )
        session.add(movie)
        session.flush()

        for g_name in m_data["genres"]:
            if g_name in genre_map:
                mg = MovieGenre(mid=movie.mid, gid=genre_map[g_name].gid)
                session.add(mg)

    session.commit()

    # Add some reviews to generate ratings
    # Trend formula: rating * 2 * review_count >= 2000 (User req)
    # This formula needs HIGH review counts (e.g. rating 5 * 2 * 200 reviews = 2000).
    # Since I can't generate 200 reviews easily, I will just add some high ratings so the Ranking works.
    # I might tweak the Trend formula in the backend code if needed, but let's add some data.

    # Give 'Inception' (id 12) a high score
    movie_inception = session.query(Movie).filter(Movie.title == "인셉션").first()
    if movie_inception:
        # Add 10 reviews
        for i in range(10):
            r = Review(
                uid=user1.uid, mid=movie_inception.mid, dec="Great movie!", rat=5.0
            )
            session.add(r)
        movie_inception.rat = 5.0  # Update avg manually for now or use logic later

    # Give 'Parasite' (id 7) high score
    movie_parasite = session.query(Movie).filter(Movie.title == "기생충").first()
    if movie_parasite:
        for i in range(5):
            r = Review(uid=user2.uid, mid=movie_parasite.mid, dec="Good!", rat=4.5)
            session.add(r)
        movie_parasite.rat = 4.5

    session.commit()
    print("Database initialized successfully.")
    session.close()


if __name__ == "__main__":
    init_db()

# MO-NO-LOG - 영화 리뷰 플랫폼

FastAPI 기반의 영화 리뷰 플랫폼입니다.

## 설치 및 실행

### 1. 의존성 설치
```bash
uv sync
```

### 2. 데이터베이스 초기화

**테이블만 생성 (데이터 없음):**
```bash
uv run python scripts/init_db.py
```

**테이블 생성 + 예시 데이터 추가:**
```bash
uv run python scripts/init_db.py --seed
```

**예시 데이터만 추가 (테이블이 이미 존재하는 경우):**
```bash
uv run python scripts/seed_data.py
```

### 3. 서버 실행
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 예시 데이터

`seed_data.py` 스크립트는 다음 예시 데이터를 추가합니다:

- **사용자 5명** (관리자 1명 포함)
- **장르 15개** (액션, 드라마, SF, 등)
- **영화 10편** (인셉션, 기생충, 인터스텔라, 등)
- **리뷰 12개**
- **댓글 10개**
- **좋아요 데이터**

### 샘플 로그인 정보
- **관리자**: `admin@mono-log.com` / `admin1234`
- **일반 사용자**: `kim@example.com` / `password123`

## API 문서

서버 실행 후 다음 주소에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조

```
app/
├── routers/         # API 라우터
│   ├── auth.py      # 인증 관련
│   ├── movies.py    # 영화 관련
│   ├── reviews.py   # 리뷰 관련
│   ├── user.py      # 사용자 관련
│   └── admin.py     # 관리자 관련
├── models.py        # SQLAlchemy ORM 모델
├── schemas.py       # Pydantic 스키마
├── database.py      # DB 연결 설정
├── dependencies.py  # FastAPI 의존성
└── utils.py         # 유틸리티 함수

scripts/
├── init_db.py       # DB 초기화 스크립트
└── seed_data.py     # 예시 데이터 추가 스크립트

web/                 # 프론트엔드 정적 파일
```

## 주의사항

⚠️ `init_db.py` 스크립트는 기존 테이블을 모두 삭제하고 재생성합니다. 운영 환경에서는 사용하지 마세요!

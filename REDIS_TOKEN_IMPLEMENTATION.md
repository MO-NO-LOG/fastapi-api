# Redis 기반 토큰 블랙리스트 및 Refresh Token 구현 (비동기)

Redis를 활용한 토큰 블랙리스트와 Refresh Token 패턴이 **비동기(async/await)** 방식으로 구현되었습니다.

## 설정

### 1. Redis 설치 및 실행

Windows에서 Redis를 설치하고 실행하세요:

```bash
# Redis를 Docker로 실행하는 경우
docker run -d -p 6379:6379 redis:latest

# 또는 Windows용 Redis 설치
# https://github.com/microsoftarchive/redis/releases
```

### 2. 환경 변수 설정

`.env` 파일에 다음 Redis 설정을 추가하세요:

```env
# 기존 설정...
DB_USER=postgres
DB_PASS=3W8EKGf4v77qr49lVf18
DB_HOST=192.168.0.41
DB_PORT=5432
DB_NAME=monolog
SECRET_KEY=supersecretkey_from_env
TMDB_API_KEY=0d18b74c03bb32be7e2aea2327e29d5b

# Redis 설정 (새로 추가)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

## 주요 기능

### 1. 토큰 블랙리스트 (Token Blacklist) - 비동기

로그아웃 시 Access Token을 블랙리스트에 추가하여 해당 토큰을 무효화합니다.

**구현 위치:**
- `app/services/token_service.py:TokenBlacklistService`
- `app/redis_client.py` - `redis.asyncio` 사용

**동작 방식:**
- 로그아웃 시 Access Token을 Redis에 **비동기**로 저장
- TTL(Time To Live)을 토큰의 남은 만료 시간으로 설정
- 토큰이 만료되면 Redis에서 자동으로 삭제됨
- 모든 Redis 작업 후 연결을 닫아 리소스 관리

**엔드포인트:**
- `POST /api/auth/logout` - 현재 토큰을 블랙리스트에 추가 (async)

### 2. Refresh Token 패턴 - 비동기

Access Token이 만료되었을 때 Refresh Token을 사용하여 새로운 토큰을 발급받습니다.

**구현 위치:**
- `app/services/token_service.py:RefreshTokenService`

**동작 방식:**
- 로그인 시 Access Token(30분) + Refresh Token(7일) 발급
- Refresh Token은 Redis에 **비동기**로 저장
- Access Token 만료 시 Refresh Token으로 새 토큰 발급
- 로그아웃 시 Refresh Token 삭제
- 각 Redis 작업 후 자동으로 연결 종료

**엔드포인트:**
- `POST /api/auth/login` - Access Token과 Refresh Token 발급 (async)
- `POST /api/auth/refresh` - Refresh Token으로 새 토큰 발급 (async)
- `POST /api/auth/logout` - 모든 토큰 무효화 (async)

### 3. 보안 강화 - 비동기

**app/dependencies.py:33** - `get_current_user` 의존성에 블랙리스트 체크 추가:

```python
# 토큰이 블랙리스트에 있는지 비동기로 확인
if await TokenBlacklistService.is_blacklisted(token):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has been revoked"
    )
```

## API 사용 예시

### 로그인
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "remember_me": false
  }'
```

**응답:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 토큰 갱신
```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -b "refresh_token=eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**응답:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### 로그아웃
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**응답:**
```json
{
  "message": "Successfully logged out"
}
```

## 파일 구조

```
app/
├── config.py                        # Redis 설정 추가 (REDIS_HOST, REDIS_PORT 등)
├── redis_client.py                  # redis.asyncio를 사용한 비동기 Redis 클라이언트
├── services/
│   └── token_service.py            # 비동기 토큰 블랙리스트 및 Refresh Token 서비스
├── routers/
│   └── auth.py                     # 비동기 로그인/로그아웃/Refresh 엔드포인트
├── dependencies.py                 # 비동기 블랙리스트 체크 추가
├── utils.py                        # Refresh Token 생성 함수 추가
└── schemas.py                      # TokenResponse, RefreshTokenRequest 스키마
```

## 비동기 처리의 장점

1. **높은 동시성**: 여러 Redis 작업을 블로킹 없이 처리
2. **성능 향상**: I/O 대기 시간 동안 다른 요청 처리 가능
3. **리소스 효율성**: 연결 풀 관리 및 자동 정리
4. **확장성**: 많은 동시 사용자를 효율적으로 처리

## 주요 비동기 함수

**Redis 서비스 (app/services/token_service.py):**
- `async def add_to_blacklist(token: str) -> bool`
- `async def is_blacklisted(token: str) -> bool`
- `async def store_refresh_token(...) -> bool`
- `async def get_refresh_token(email: str) -> Optional[str]`
- `async def verify_refresh_token(...) -> bool`
- `async def delete_refresh_token(email: str) -> bool`

**인증 엔드포인트 (app/routers/auth.py):**
- `async def login(...)`
- `async def logout(...)`
- `async def refresh_access_token(...)`

**의존성 (app/dependencies.py):**
- `async def get_current_user(...)`

## 보안 고려사항

1. **HTTPS 사용**: 프로덕션에서는 반드시 `secure=True`로 설정
2. **Redis 보안**: Redis에 비밀번호 설정 권장
3. **토큰 만료 시간**: 
   - Access Token: 30분 (짧게 유지)
   - Refresh Token: 7일 (remember_me와 무관하게 고정)
4. **Single Device Login**: 현재 구현은 사용자당 하나의 Refresh Token만 저장 (마지막 로그인 세션만 유효)
5. **연결 관리**: 각 Redis 작업 후 `aclose()`로 자동 연결 종료

## Redis 데이터 확인

Redis CLI로 저장된 데이터를 확인할 수 있습니다:

```bash
# Redis CLI 접속
redis-cli

# 블랙리스트 확인
KEYS blacklist:*

# Refresh Token 확인
KEYS refresh_token:*

# 특정 키의 값 확인
GET refresh_token:user@example.com

# TTL 확인
TTL blacklist:eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 트러블슈팅

### Redis 연결 오류
- Redis 서버가 실행 중인지 확인
- `.env` 파일의 `REDIS_HOST`와 `REDIS_PORT` 확인
- 방화벽 설정 확인

### 토큰이 무효화되지 않음
- Redis 서버가 정상 작동하는지 확인
- `TokenBlacklistService.is_blacklisted()` 로그 확인

### Refresh Token이 작동하지 않음
- Redis에 Refresh Token이 저장되어 있는지 확인
- 토큰의 `type` 필드가 "refresh"인지 확인

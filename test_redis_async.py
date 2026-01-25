"""
비동기 Redis 토큰 서비스 테스트 스크립트

이 스크립트는 Redis 연결 및 토큰 서비스의 기본 동작을 테스트합니다.
"""

import asyncio
from app.redis_client import get_redis_client
from app.services.token_service import TokenBlacklistService, RefreshTokenService
from app.utils import create_access_token, create_refresh_token
from datetime import timedelta


async def test_redis_connection():
    """Redis 연결 테스트"""
    print("=" * 60)
    print("1. Redis 연결 테스트")
    print("=" * 60)

    redis_client = None
    try:
        redis_client = get_redis_client()
        await redis_client.ping()
        print("✓ Redis 연결 성공!")
        return True
    except Exception as e:
        print(f"✗ Redis 연결 실패: {e}")
        return False
    finally:
        if redis_client:
            await redis_client.aclose()


async def test_token_blacklist():
    """토큰 블랙리스트 테스트"""
    print("\n" + "=" * 60)
    print("2. 토큰 블랙리스트 테스트")
    print("=" * 60)

    # 테스트용 토큰 생성
    test_token = create_access_token(
        data={"sub": "test@example.com"}, expires_delta=timedelta(minutes=5)
    )
    print(f"테스트 토큰 생성: {test_token[:50]}...")

    # 블랙리스트에 추가
    result = await TokenBlacklistService.add_to_blacklist(test_token)
    if result:
        print("✓ 토큰을 블랙리스트에 추가 성공")
    else:
        print("✗ 토큰 블랙리스트 추가 실패")
        return False

    # 블랙리스트 확인
    is_blacklisted = await TokenBlacklistService.is_blacklisted(test_token)
    if is_blacklisted:
        print("✓ 토큰이 블랙리스트에 있음을 확인")
    else:
        print("✗ 토큰이 블랙리스트에 없음")
        return False

    # 블랙리스트에서 제거
    removed = await TokenBlacklistService.remove_from_blacklist(test_token)
    if removed:
        print("✓ 토큰을 블랙리스트에서 제거 성공")
    else:
        print("✗ 토큰 블랙리스트 제거 실패")
        return False

    # 제거 확인
    is_blacklisted = await TokenBlacklistService.is_blacklisted(test_token)
    if not is_blacklisted:
        print("✓ 토큰이 블랙리스트에서 제거되었음을 확인")
    else:
        print("✗ 토큰이 여전히 블랙리스트에 있음")
        return False

    return True


async def test_refresh_token():
    """Refresh Token 테스트"""
    print("\n" + "=" * 60)
    print("3. Refresh Token 서비스 테스트")
    print("=" * 60)

    test_email = "test@example.com"

    # Refresh Token 생성
    refresh_token = create_refresh_token(
        data={"sub": test_email}, expires_delta=timedelta(days=7)
    )
    print(f"Refresh Token 생성: {refresh_token[:50]}...")

    # Refresh Token 저장
    result = await RefreshTokenService.store_refresh_token(
        email=test_email,
        refresh_token=refresh_token,
        expires_delta=timedelta(minutes=1),  # 테스트용으로 1분 설정
    )
    if result:
        print(f"✓ Refresh Token 저장 성공 (email: {test_email})")
    else:
        print("✗ Refresh Token 저장 실패")
        return False

    # Refresh Token 조회
    stored_token = await RefreshTokenService.get_refresh_token(test_email)
    if stored_token == refresh_token:
        print("✓ Refresh Token 조회 성공")
    else:
        print("✗ Refresh Token 조회 실패")
        return False

    # Refresh Token 검증
    is_valid = await RefreshTokenService.verify_refresh_token(test_email, refresh_token)
    if is_valid:
        print("✓ Refresh Token 검증 성공")
    else:
        print("✗ Refresh Token 검증 실패")
        return False

    # 잘못된 토큰 검증
    is_valid = await RefreshTokenService.verify_refresh_token(test_email, "wrong_token")
    if not is_valid:
        print("✓ 잘못된 Refresh Token 거부 확인")
    else:
        print("✗ 잘못된 Refresh Token이 허용됨")
        return False

    # Refresh Token 삭제
    deleted = await RefreshTokenService.delete_refresh_token(test_email)
    if deleted:
        print(f"✓ Refresh Token 삭제 성공 (email: {test_email})")
    else:
        print("✗ Refresh Token 삭제 실패")
        return False

    # 삭제 확인
    stored_token = await RefreshTokenService.get_refresh_token(test_email)
    if stored_token is None:
        print("✓ Refresh Token이 삭제되었음을 확인")
    else:
        print("✗ Refresh Token이 여전히 존재함")
        return False

    return True


async def main():
    """메인 테스트 함수"""
    print("\n" + "=" * 60)
    print("Redis 비동기 토큰 서비스 테스트")
    print("=" * 60)

    # Redis 연결 테스트
    if not await test_redis_connection():
        print("\n❌ Redis 연결 실패. Redis 서버가 실행 중인지 확인하세요.")
        return

    # 토큰 블랙리스트 테스트
    if not await test_token_blacklist():
        print("\n❌ 토큰 블랙리스트 테스트 실패")
        return

    # Refresh Token 테스트
    if not await test_refresh_token():
        print("\n❌ Refresh Token 테스트 실패")
        return

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 통과!")
    print("=" * 60)
    print("\n다음 단계:")
    print("1. Redis 서버가 실행 중인지 확인: docker run -d -p 6379:6379 redis:latest")
    print("2. 서버 실행: uv run uvicorn app.main:app --reload")
    print("3. API 테스트: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    asyncio.run(main())

"""JWT 인증(get_current_user)이 완성되기 전까지 사용하는 임시 로그인 사용자 확인입니다.

`app.core.security.get_current_user`가 준비되면 이 파일을 삭제하고
routes에서 `from app.core.security import get_current_user`로 교체합니다.
교체 시 response의 user_id 타입도 의존성의 반환 타입에 맞춰야 합니다.
"""

from fastapi import HTTPException, status

from app.core.settings import settings


def get_current_user_id() -> int:
    """임시 로그인 사용자 확인 의존성입니다. SECRET_KEY가 없으면 401, 그 외에는 501을 반환합니다."""
    if settings.secret_key == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT 인증 설정이 없습니다. .env에 SECRET_KEY가 필요합니다.",
        )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="로그인 사용자 확인은 아름 담당의 JWT 구현 후 연결됩니다.",
    )

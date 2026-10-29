"""아름 님의 공통 인증을 호출합니다. JWT 검증 자체는 이 파일에서 구현하지 않습니다."""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.models.user import User
from app.db.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


def get_schedule_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="로그인이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 아직 함수가 없는 main에서도 라우터를 불러올 수 있도록 요청 시 가져옵니다.
    # 인증 함수의 약속: get_current_user(token=문자열, db=세션) -> User
    from app.core import security

    authenticate = getattr(security, "get_current_user", None)
    if authenticate is None:
        raise HTTPException(status_code=503, detail="공통 JWT 인증 연결이 준비되지 않았습니다.")
    return authenticate(token=token, db=db)

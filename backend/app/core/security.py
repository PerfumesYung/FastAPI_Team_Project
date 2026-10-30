"""비밀번호 해시와 JWT 발급·검증을 담당합니다."""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.models.user import User
from app.core.settings import settings
from app.db.database import get_db


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    auto_error=False,
)


def get_secret_key() -> str:
    # .env의 SECRET_KEY는 소문자 속성으로 읽습니다.
    secret_key = settings.secret_key.strip()

    if not secret_key:
        raise HTTPException(
            status_code=503,
            detail="JWT 비밀키가 설정되지 않았습니다.",
        )

    return secret_key


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    payload = data.copy()

    # .env의 ACCESS_TOKEN_EXPIRE_MINUTES 값을 분 단위로 적용합니다.
    lifetime = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )

    payload["exp"] = datetime.now(timezone.utc) + lifetime

    return jwt.encode(
        payload,
        get_secret_key(),
        algorithm=ALGORITHM,
    )


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    headers = {"WWW-Authenticate": "Bearer"}

    if not token:
        raise HTTPException(
            status_code=401,
            detail="로그인이 필요합니다.",
            headers=headers,
        )

    secret_key = get_secret_key()

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[ALGORITHM],
            options={
                "require_exp": True,
                "require_sub": True,
            },
        )

        email = payload.get("sub")

        if not isinstance(email, str) or not email:
            raise JWTError("사용자 정보가 없습니다.")

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="만료된 토큰입니다. 다시 로그인해 주세요.",
            headers=headers,
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 토큰입니다.",
            headers=headers,
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="토큰에 해당하는 사용자가 없습니다.",
            headers=headers,
        )

    return user
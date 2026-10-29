from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.settings import settings
from app.db.database import get_db
from app.auth.models.user import User


# 비밀번호 보안 강화를 위해 bcrypt 암호화 콘텍스트 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Swagger UI 연동 및 Authorization Bearer 헤더 추출용 인스턴스
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

SECRET_KEY = getattr(settings, "SECRET_KEY", "YOUR_SECRET_KEY_MUST_BE_OVER_32_BYTES_LONG")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  #기획안 세부 지침: 인증 토큰은 30분 만료 적용

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #사용자가 입력한 평문 암호와 DB의 해시 암호가 일치하는지 안전하게 검증합니다
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    #회원가입 시 유저의 평문 비밀번호를 해시값으로 변환합니다
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    #로그인 유저를 식별하기 위한 고유 JWT 액세스 토큰을 발행합니다 (만료시간 포함)
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # 1. 헤더에 토큰이 없는 접근 차단
    if not token:
        raise HTTPException(status_code=401, detail="인증 토큰이 누락되었습니다. 로그인이 필요합니다.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰 구조입니다.")
    # 2. 만료된 토큰 거절 예외 처리
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="만료된 토큰입니다. 다시 로그인 해주세요.")
    # 3. 위조 및 변조된 토큰 거절 예외 처리
    except JWTError:
        raise HTTPException(status_code=401, detail="변조되거나 신뢰할 수 없는 토큰입니다.")
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="토큰과 일치하는 사용자 정보가 존재하지 않습니다.")
    return user
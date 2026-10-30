from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.models import User
from app.auth.schemas import UserCreate, UserRead, Token
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    #이메일 중복 거절 확인
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=409, detail="이미 존재하는 이메일 계정입니다.")
    #사용자명 중복 거절 확인
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=409, detail="이미 사용 중인 사용자명입니다.")

    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password), # 비밀번호 암호화 저장
        role="USER"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    #계정이 없거나 암호 대조 결과가 올바르지 않은 경우
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
        
    return {"access_token": create_access_token(data={"sub": user.email}), "token_type": "bearer"}

@router.get("/users/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
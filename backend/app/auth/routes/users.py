from fastapi import APIRouter, HTTPException


# /users로 시작하는 회원 관련 경로
router = APIRouter(
    prefix="/users",
    tags=["회원"],
)

# /auth로 시작하는 인증 관련 경로
auth_router = APIRouter(
    prefix="/auth",
    tags=["인증"],
)


# 회원가입
# POST /users
@router.post("")
def create_user():
    raise HTTPException(
        status_code=501,
        detail="회원가입 기능 구현 예정",
    )


# 내 정보 조회
# GET /users/me
@router.get("/me")
def read_my_info():
    raise HTTPException(
        status_code=501,
        detail="내 정보 조회 기능 구현 예정",
    )


# 로그인 및 토큰 발급
# POST /auth/token
@auth_router.post("/token")
def login():
    raise HTTPException(
        status_code=501,
        detail="로그인 기능 구현 예정",
    )
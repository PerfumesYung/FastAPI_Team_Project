from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/categories",
    tags=["카테고리"],
)


# 카테고리 목록 조회
# GET /categories
@router.get("")
def read_categories():
    raise HTTPException(
        status_code=501,
        detail="카테고리 조회 기능 구현 예정",
    )
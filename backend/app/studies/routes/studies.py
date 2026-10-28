from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/studies",
    tags=["스터디"],
)


# 스터디 목록 조회
# GET /studies
@router.get("")
def read_studies():
    raise HTTPException(
        status_code=501,
        detail="스터디 목록 조회 기능 구현 예정",
    )


# 스터디 생성
# POST /studies
@router.post("")
def create_study():
    raise HTTPException(
        status_code=501,
        detail="스터디 생성 기능 구현 예정",
    )


# 스터디 상세 조회
# GET /studies/1
@router.get("/{study_id}")
def read_study(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="스터디 상세 조회 기능 구현 예정",
    )


# 스터디 수정
# PUT /studies/1
@router.put("/{study_id}")
def update_study(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="스터디 수정 기능 구현 예정",
    )


# 스터디 삭제
# DELETE /studies/1
@router.delete("/{study_id}")
def delete_study(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="스터디 삭제 기능 구현 예정",
    )
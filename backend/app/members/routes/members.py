from fastapi import APIRouter, HTTPException


# 스터디 참가 관련 경로
router = APIRouter(
    prefix="/studies",
    tags=["참가"],
)

# 내가 참가한 스터디 조회용 경로
my_studies_router = APIRouter(
    prefix="/users/me",
    tags=["참가"],
)


# 스터디 참가
# POST /studies/1/members
@router.post("/{study_id}/members")
def join_study(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="스터디 참가 기능 구현 예정",
    )


# 내 참가 취소
# DELETE /studies/1/members/me
@router.delete("/{study_id}/members/me")
def leave_study(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="스터디 참가 취소 기능 구현 예정",
    )


# 스터디 참가자 목록
# GET /studies/1/members
@router.get("/{study_id}/members")
def read_study_members(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="참가자 목록 조회 기능 구현 예정",
    )


# 내가 참가한 스터디 목록
# GET /users/me/studies
@my_studies_router.get("/studies")
def read_my_studies():
    raise HTTPException(
        status_code=501,
        detail="내 참가 스터디 조회 기능 구현 예정",
    )
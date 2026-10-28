from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/studies",
    tags=["일정"],
)


# 스터디 일정 목록 조회
# GET /studies/1/schedules
@router.get("/{study_id}/schedules")
def read_schedules(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="일정 목록 조회 기능 구현 예정",
    )


# 스터디 일정 등록
# POST /studies/1/schedules
@router.post("/{study_id}/schedules")
def create_schedule(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="일정 등록 기능 구현 예정",
    )


# 스터디 일정 수정
# PUT /studies/1/schedules/2
@router.put("/{study_id}/schedules/{schedule_id}")
def update_schedule(study_id: int, schedule_id: int):
    raise HTTPException(
        status_code=501,
        detail="일정 수정 기능 구현 예정",
    )


# 스터디 일정 삭제
# DELETE /studies/1/schedules/2
@router.delete("/{study_id}/schedules/{schedule_id}")
def delete_schedule(study_id: int, schedule_id: int):
    raise HTTPException(
        status_code=501,
        detail="일정 삭제 기능 구현 예정",
    )
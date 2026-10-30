"""공통 JWT 인증으로 로그인 사용자를 확인하고,
사용자 번호(current_user.id)를 참가 서비스에 전달합니다.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.members.schemas.member import MemberResponse, MyStudyListResponse, ParticipantListResponse
from app.members.services import build_my_study_list, build_participant_list, join_study, leave_study
from app.auth.models.user import User
from app.core.security import get_current_user

# OpenAPI에 표시할 오류 응답 명세
NOT_FOUND = {"description": "스터디 또는 참가 기록이 없음"}
CLOSED = {"description": "모집이 마감된 스터디"}
CONFLICT = {"description": "중복 참가 또는 정원 초과"}

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
# POST /studies/{study_id}/members
@router.post(
    "/{study_id}/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: NOT_FOUND,
        status.HTTP_400_BAD_REQUEST: CLOSED,
        status.HTTP_409_CONFLICT: CONFLICT,
    },
)
def add_study_member(
    study_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return join_study(db, study_id, current_user.id)


# 내 참가 취소
# DELETE /studies/{study_id}/members/me
@router.delete(
    "/{study_id}/members/me",
    response_model=MemberResponse,
    responses={
        status.HTTP_404_NOT_FOUND: NOT_FOUND,
        status.HTTP_401_UNAUTHORIZED: {"description": "로그인 필요"},
    },
)
def remove_my_study_member(
    study_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return leave_study(db, study_id, current_user.id)


# 스터디 참가자 목록
# GET /studies/{study_id}/members
@router.get(
    "/{study_id}/members",
    response_model=ParticipantListResponse,
    responses={status.HTTP_404_NOT_FOUND: NOT_FOUND},
)
def read_study_members(study_id: int, db: Session = Depends(get_db)):
    return build_participant_list(db, study_id)


# 내가 참가한 스터디 목록
# GET /users/me/studies
@my_studies_router.get(
    "/studies",
    response_model=MyStudyListResponse,
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "로그인 필요"}},
)
def read_my_studies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return build_my_study_list(db, current_user.id)

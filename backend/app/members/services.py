"""참가 관련 DB 처리를 담당하는 서비스 계층입니다.

routes는 요청/응답(엔포인트)만 담당하고, DB 조회·검증 로직은 이곳에서 처리합니다.
서비스는 HTTPException을 직접 발생시킵니다.
"""

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.models.user import User
from app.members.models.member import StudyMember
from app.members.schemas.member import (
    MyStudy,
    MyStudyListResponse,
    ParticipantListResponse,
    StudyParticipant,
)
from app.studies.models.study import StudyGroup


def find_study(db: Session, study_id: int) -> StudyGroup:
    """경로 매개변수로 받은 스터디를 조회합니다. 없으면 404를 발생시킵니다."""
    study = db.get(StudyGroup, study_id)
    if study is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"스터디 {study_id}가 없습니다.",
        )
    return study


def count_participants(db: Session, study_id: int) -> int:
    """스터디의 현재 참가 수를 셉니다."""
    return db.scalar(
        select(func.count())
        .select_from(StudyMember)
        .where(StudyMember.study_id == study_id)
    )


def find_membership(db: Session, study_id: int, user_id: int) -> StudyMember | None:
    """특정 사용자의 참가 기록을 조회합니다. 없으면 None입니다."""
    return db.scalar(
        select(StudyMember)
        .where(StudyMember.study_id == study_id)
        .where(StudyMember.user_id == user_id)
    )


def join_study(db: Session, study_id: int, user_id: int) -> StudyMember:
    """스터디에 참가합니다. 마감·중복·정원 조건은 HTTPException으로 거부합니다."""
    study = find_study(db, study_id)

    # 모집이 마감된 스터디
    if study.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="모집이 마감된 스터디입니다.",
        )

    # 중복 참가 방지
    if find_membership(db, study_id, user_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 참가한 스터디입니다.",
        )

    # 정원 확인
    if count_participants(db, study_id) >= study.max_members:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="정원이 가득 찼습니다.",
        )

    member = StudyMember(user_id=user_id, study_id=study_id)
    db.add(member)
    try:
        db.commit()
    except IntegrityError:
        # 동시 요청으로 유니크 제약(uq_study_members_user_study)에 걸린 경우
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 참가한 스터디입니다.",
        )
    db.refresh(member)
    return member


def build_participant_list(db: Session, study_id: int) -> ParticipantListResponse:
    """참가자 목록 응답을 조립합니다. 없으면 404를 발생시킵니다."""
    study = find_study(db, study_id)

    rows = db.execute(
        select(User.id, User.username, StudyMember.joined_at)
        .join(StudyMember, StudyMember.user_id == User.id)
        .where(StudyMember.study_id == study_id)
        .order_by(StudyMember.joined_at)
    )

    return ParticipantListResponse(
        study_id=study.id,
        max_members=study.max_members,
        participants=[
            StudyParticipant(user_id=row.id, username=row.username, joined_at=row.joined_at)
            for row in rows
        ],
    )


def build_my_study_list(db: Session, user_id: int) -> MyStudyListResponse:
    """내가 참가한 스터디 목록을 joined_at 순으로 조립합니다."""
    rows = db.execute(
        select(StudyGroup, StudyMember.joined_at)
        .join(StudyMember, StudyMember.study_id == StudyGroup.id)
        .where(StudyMember.user_id == user_id)
        .order_by(StudyMember.joined_at)
    )

    return MyStudyListResponse(
        studies=[
            MyStudy(
                study_id=study.id,
                title=study.title,
                status=study.status,
                max_members=study.max_members,
                joined_at=joined_at,
            )
            for study, joined_at in rows
        ],
    )


def leave_study(db: Session, study_id: int, user_id: int) -> StudyMember:
    """본인의 스터디 참가를 취소합니다. 참가 기록이 없으면 404를 발생시킵니다."""
    study = find_study(db, study_id)

    member = find_membership(db, study.id, user_id)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="참가한 스터디가 아닙니다.",
        )

    db.delete(member)
    db.commit()
    return member

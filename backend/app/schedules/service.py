"""일정 전용 DB 처리입니다. 다른 담당자의 service 파일에 의존하지 않습니다."""
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schedules.models.schedule import StudySchedule
from app.schedules.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.studies.models.study import StudyGroup


def find_study(db: Session, study_id: int) -> StudyGroup:
    study = db.get(StudyGroup, study_id)
    if study is None:
        raise HTTPException(status_code=404, detail="스터디를 찾을 수 없습니다.")
    return study


def require_owner(study: StudyGroup, user_id: int) -> None:
    if study.owner_id != user_id:
        raise HTTPException(status_code=403, detail="스터디 작성자만 일정을 변경할 수 있습니다.")


def find_schedule(db: Session, study_id: int, schedule_id: int) -> StudySchedule:
    schedule = db.get(StudySchedule, schedule_id)
    # 다른 스터디의 일정 ID를 넣어 수정·삭제하는 요청도 차단합니다.
    if schedule is None or schedule.study_id != study_id:
        raise HTTPException(status_code=404, detail="해당 스터디의 일정을 찾을 수 없습니다.")
    return schedule


def read_schedules(db: Session, study_id: int) -> list[StudySchedule]:
    find_study(db, study_id)
    return list(db.scalars(
        select(StudySchedule)
        .where(StudySchedule.study_id == study_id)
        .order_by(StudySchedule.starts_at, StudySchedule.id)
    ))


def save_schedule(db: Session, schedule: StudySchedule) -> StudySchedule:
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(schedule)
    return schedule


def create_schedule(
    db: Session, study_id: int, data: ScheduleCreate, user_id: int,
) -> StudySchedule:
    require_owner(find_study(db, study_id), user_id)
    schedule = StudySchedule(
        study_id=study_id,
        title=data.title,
        # UTC 변환된 값에서 시간대 표기만 제거해 기존 DateTime 컬럼에 저장합니다.
        starts_at=data.starts_at.replace(tzinfo=None),
        location=data.location,
    )
    db.add(schedule)
    return save_schedule(db, schedule)


def update_schedule(
    db: Session, study_id: int, schedule_id: int, data: ScheduleUpdate, user_id: int,
) -> StudySchedule:
    require_owner(find_study(db, study_id), user_id)
    schedule = find_schedule(db, study_id, schedule_id)
    schedule.title = data.title
    schedule.starts_at = data.starts_at.replace(tzinfo=None)
    schedule.location = data.location
    return save_schedule(db, schedule)


def delete_schedule(db: Session, study_id: int, schedule_id: int, user_id: int) -> None:
    require_owner(find_study(db, study_id), user_id)
    schedule = find_schedule(db, study_id, schedule_id)
    db.delete(schedule)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

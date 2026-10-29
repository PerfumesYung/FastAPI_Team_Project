"""경로 → 입력·인증 확인 → service → 응답 순서로 처리합니다."""
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status
from sqlalchemy.orm import Session

from app.auth.models.user import User
from app.db.database import get_db
from app.schedules import service
from app.schedules.dependencies import get_schedule_user
from app.schedules.schemas.schedule import ScheduleCreate, ScheduleRead, ScheduleUpdate


router = APIRouter(prefix="/studies", tags=["일정"])
PositiveId = Annotated[int, Path(gt=0)]
Database = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_schedule_user)]


@router.get("/{study_id}/schedules", response_model=list[ScheduleRead])
def read_schedules(study_id: PositiveId, db: Database):
    return service.read_schedules(db, study_id)


@router.post(
    "/{study_id}/schedules",
    response_model=ScheduleRead,
    status_code=status.HTTP_201_CREATED,
)
def create_schedule(study_id: PositiveId, data: ScheduleCreate, db: Database, current_user: CurrentUser):
    return service.create_schedule(db, study_id, data, current_user.id)


@router.put("/{study_id}/schedules/{schedule_id}", response_model=ScheduleRead)
def update_schedule(
    study_id: PositiveId, schedule_id: PositiveId, data: ScheduleUpdate,
    db: Database, current_user: CurrentUser,
):
    return service.update_schedule(db, study_id, schedule_id, data, current_user.id)


@router.delete("/{study_id}/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(study_id: PositiveId, schedule_id: PositiveId, db: Database, current_user: CurrentUser):
    service.delete_schedule(db, study_id, schedule_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

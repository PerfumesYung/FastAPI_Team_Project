"""일정 입력 검증과 응답 형식입니다. 기존 DB 컬럼명을 사용합니다."""
from datetime import datetime, timezone

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator


class ScheduleCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=150)
    starts_at: AwareDatetime
    location: str = Field(min_length=1, max_length=255)

    @field_validator("starts_at")
    @classmethod
    def normalize_to_utc(cls, value: datetime) -> datetime:
        # 시간대가 포함된 입력을 UTC로 변환합니다.
        return value.astimezone(timezone.utc)


class ScheduleUpdate(ScheduleCreate):
    """PUT 요청이므로 등록과 동일하게 세 필드 전체를 받습니다."""


class ScheduleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    study_id: int
    title: str
    starts_at: datetime
    location: str

    @field_validator("starts_at")
    @classmethod
    def include_utc_timezone(cls, value: datetime) -> datetime:
        # DB에 저장한 시간대 없는 UTC에 응답용 시간대 정보를 붙입니다.
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StudySchedule(Base):
    __tablename__ = "study_schedules"

    # 일정 번호
    id: Mapped[int] = mapped_column(primary_key=True)

    # 일정이 속한 스터디 번호
    # 스터디 삭제 시 관련 일정도 함께 삭제되도록 설정
    study_id: Mapped[int] = mapped_column(
        ForeignKey(
            "study_groups.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # 일정 제목
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # 일정 시작 시각
    # 어떤 시간대를 받아 UTC로 변환할지는 일정 담당자와 합의
    starts_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # 일정 장소
    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    # 시간대 정보가 없는 UTC 시각을 저장
    return datetime.now(timezone.utc).replace(tzinfo=None)


class StudyMember(Base):
    __tablename__ = "study_members"

    __table_args__ = (
        # 같은 사용자가 같은 스터디에 중복 참가하지 못하도록 제한
        # user_id와 study_id의 "조합"이 중복되면 안 됨
        UniqueConstraint(
            "user_id",
            "study_id",
            name="uq_study_members_user_study",
        ),
    )

    # 참가 기록 번호
    id: Mapped[int] = mapped_column(primary_key=True)

    # 참가한 사용자 번호
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # 참가한 스터디 번호
    # 스터디가 삭제되면 관련 참가 기록도 삭제되도록 설정
    study_id: Mapped[int] = mapped_column(
        ForeignKey(
            "study_groups.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # 참가한 시각
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )
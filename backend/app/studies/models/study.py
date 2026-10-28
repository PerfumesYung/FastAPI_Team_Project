from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    """
    현재 UTC 시각을 반환합니다.

    DB에는 시간대 정보가 없는 UTC 시각으로 저장합니다.
    시간대 변환 규칙은 API 담당자와 함께 맞춰야 합니다.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class StudyGroup(Base):
    __tablename__ = "study_groups"

    # 테이블에 적용할 제약조건
    __table_args__ = (
        # 최대 인원은 0보다 커야 함
        CheckConstraint(
            "max_members > 0",
            name="ck_study_groups_max_members",
        ),

        # 상태는 OPEN 또는 CLOSED만 허용
        CheckConstraint(
            "status IN ('OPEN', 'CLOSED')",
            name="ck_study_groups_status",
        ),
    )

    # 스터디 번호
    id: Mapped[int] = mapped_column(primary_key=True)

    # 스터디 제목
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # 스터디 소개
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # 최대 참가 인원
    max_members: Mapped[int] = mapped_column(
        nullable=False,
    )

    # 작성자 번호
    # users 테이블의 id를 참조
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # 카테고리 번호
    # study_categories 테이블의 id를 참조
    category_id: Mapped[int] = mapped_column(
        ForeignKey("study_categories.id"),
        nullable=False,
    )

    # 모집 상태: OPEN 또는 CLOSED
    status: Mapped[str] = mapped_column(
        String(10),
        default="OPEN",
        nullable=False,
    )

    # 스터디 생성 시각
    # SQLAlchemy가 INSERT할 때 utc_now()를 호출
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )
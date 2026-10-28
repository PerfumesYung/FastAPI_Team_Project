from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StudyCategory(Base):
    __tablename__ = "study_categories"

    # 카테고리 번호
    id: Mapped[int] = mapped_column(primary_key=True)

    # 카테고리명
    # 예: Backend, Frontend, Algorithm
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
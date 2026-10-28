from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    # 실제 DB에서 사용할 테이블 이름
    __tablename__ = "users"

    # 사용자 번호: 기본키
    id: Mapped[int] = mapped_column(primary_key=True)

    # 이메일: 중복 불가, 필수
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    # 사용자명: 중복 불가, 필수
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    # 비밀번호 원문이 아닌 해시값을 저장
    # 해시를 만드는 기능은 인증 담당자가 구현
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # 사용자의 권한
    # 값을 지정하지 않고 SQLAlchemy로 저장하면 USER 사용
    role: Mapped[str] = mapped_column(
        String(20),
        default="USER",
        nullable=False,
    )
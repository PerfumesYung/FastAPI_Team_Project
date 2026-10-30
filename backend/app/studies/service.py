from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.studies.models.category import StudyCategory
from app.studies.models.study import StudyGroup
from app.studies.schemas.study import StudyCreate, StudyUpdate


class StudyService:
    # 스터디 목록 조회
    @staticmethod
    def get_studies(
        db: Session,
        keyword: str | None = None,
        category_id: int | None = None,
        status: str | None = None,
    ):
        query = db.query(StudyGroup)

        # 검색어는 제목 또는 소개에서 찾고, 여러 필터는 AND로 조합합니다.
        if keyword and keyword.strip():
            word = keyword.strip()
            query = query.filter(or_(
                StudyGroup.title.contains(word, autoescape=True),
                StudyGroup.description.contains(word, autoescape=True),
            ))
        if category_id is not None:
            query = query.filter(StudyGroup.category_id == category_id)
        if status is not None:
            query = query.filter(StudyGroup.status == status)

        return query.order_by(StudyGroup.id).all()

    # 스터디 상세 조회
    @staticmethod
    def get_study(db: Session, study_id: int):
        study = (db.query(StudyGroup).filter(StudyGroup.id == study_id).first())

        if study is None:
            raise HTTPException(status_code=404,detail="스터디를 찾을 수 없습니다.",)
        return study

    # 스터디 생성
    @staticmethod
    def add_study(db: Session,study: StudyCreate,owner_id: int):
        category = (db.query(StudyCategory).filter(StudyCategory.id == study.category_id).first())

        if category is None:
            raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

        db_study = StudyGroup(title=study.title,description=study.description,
            max_members=study.max_members,category_id=study.category_id,owner_id=owner_id,
        )
        db.add(db_study)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(db_study)
        return db_study

    # 스터디 수정
    @staticmethod
    def update_study(db: Session,study_id: int,study: StudyUpdate, user_id: int):
        db_study = StudyService.get_study(db, study_id)

        if db_study.owner_id != user_id:
            raise HTTPException(status_code=403, detail="작성자만 수정할 수 있습니다.",
        )
        db_study.title = study.title
        db_study.description = study.description
        db_study.max_members = study.max_members
        db_study.status = study.status

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(db_study)
        return db_study

    # 스터디 삭제
    @staticmethod
    def delete_study(db: Session, study_id: int, user_id):
        db_study = StudyService.get_study(db, study_id)

        if db_study.owner_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="작성자만 삭제할 수 있습니다.",
        )
        db.delete(db_study)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

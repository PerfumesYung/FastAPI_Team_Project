from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.studies.models.category import StudyCategory
from app.studies.schemas.category import StudyCategoryCreate
from sqlalchemy.future import select

router = APIRouter(
    prefix="/categories",
    tags=["카테고리"],
)


# 카테고리 목록 조회
# GET /categories
@router.get("", response_model=list[StudyCategoryCreate])
def read_categories(db: Session= Depends(get_db)):
    db_study_categories = select(StudyCategory).order_by(StudyCategory.id)
    return db.scalars(db_study_categories).all()


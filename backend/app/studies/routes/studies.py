from typing import Literal

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.studies.schemas.study import StudyCreate, StudyResponse, StudyUpdate
from app.studies.service import StudyService
from app.core.security import get_current_user


router = APIRouter(
    prefix="/studies",tags=["스터디"],
)
#UserStudy 메소드, add_study, get_study_id, update_study


# 스터디 목록 조회
# GET /studies
@router.get("", response_model=list[StudyResponse])
def read_studies(
    db: Session = Depends(get_db),
    keyword: str | None = Query(None, min_length=1, max_length=150, description="제목·소개 검색어"),
    category_id: int | None = Query(None, gt=0, description="카테고리 번호"),
    status: Literal["OPEN", "CLOSED"] | None = Query(None, description="모집 상태"),
):
    # Query를 생략하면 기존처럼 전체 목록을 반환합니다.
    return StudyService.get_studies(db, keyword, category_id, status)

# 스터디 생성
# POST /studies 
@router.post("", response_model = StudyResponse)
def create_study(study: StudyCreate, current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    db_study= StudyService.add_study(db, study, current_user.id)
    return db_study


# 스터디 상세 조회
# GET /studies/1
@router.get("/{study_id}", response_model=StudyResponse)
def read_study(study_id: int, db: Session = Depends(get_db)):
    db_study= StudyService.get_study(db, study_id)
    return db_study
    

# 스터디 수정
# PUT /studies/1
@router.put("/{study_id}",   response_model= StudyResponse)
def update_study(study_id: int, study: StudyUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_study =StudyService.update_study(db, study_id, study, current_user.id)
    return db_study

# 스터디 삭제
# DELETE /studies/1
@router.delete("/{study_id}")
def delete_study(study_id: int, current_user=Depends(get_current_user),  db: Session = Depends(get_db)):
    StudyService.delete_study(db, study_id, current_user.id)
    return Response(status_code=204)

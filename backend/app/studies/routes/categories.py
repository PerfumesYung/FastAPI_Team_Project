"""카테고리 목록 등 필요한 경로

TODO: router에 필요한 API를 추가하세요.
DB 세션이 필요한 경로는 app.db.database.get_db를 사용합니다.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/categories", tags=["카테고리"])

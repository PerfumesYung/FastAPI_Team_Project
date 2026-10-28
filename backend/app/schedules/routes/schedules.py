"""스터디 일정 등록·조회 등 합의한 기능

TODO: router에 필요한 API를 추가하세요.
DB 세션이 필요한 경로는 app.db.database.get_db를 사용합니다.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/studies", tags=["일정"])

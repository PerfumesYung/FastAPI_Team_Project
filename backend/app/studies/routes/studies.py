"""스터디 생성·조회·검색·수정·삭제. Path·Query·Body를 사용하세요.

TODO: router에 필요한 API를 추가하세요.
DB 세션이 필요한 경로는 app.db.database.get_db를 사용합니다.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/studies", tags=["스터디"])

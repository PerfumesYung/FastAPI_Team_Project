"""스터디 참가·취소·참가자 조회. 인증과 정원 규칙을 팀과 합의하세요.

TODO: router에 필요한 API를 추가하세요.
DB 세션이 필요한 경로는 app.db.database.get_db를 사용합니다.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/studies", tags=["참가"])

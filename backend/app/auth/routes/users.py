"""회원가입·로그인·내 정보. 로그인 경로와 OAuth2 tokenUrl은 팀 합의 후 맞추세요.

TODO: router에 필요한 API를 추가하세요.
DB 세션이 필요한 경로는 app.db.database.get_db를 사용합니다.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["회원 / 인증"])

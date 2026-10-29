from auth.routes.users import router as auth_router

#auth/security.py 파일 안의 핵심 인증 함수를 가져옵니다.
from .security import get_current_user
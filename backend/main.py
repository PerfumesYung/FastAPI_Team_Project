from fastapi import FastAPI

# 각 담당자가 작업할 라우터 파일을 가져옴
from app.auth.routes import users
from app.studies.routes import studies, categories
from app.members.routes import members
from app.schedules.routes import schedules


# FastAPI 앱 생성
app = FastAPI(
    title="스터디 관리 API",
)


# 회원·인증
app.include_router(users.router)
app.include_router(users.auth_router)

# 스터디·카테고리
app.include_router(studies.router)
app.include_router(categories.router)

# 참가·내 참가 목록
app.include_router(members.router)
app.include_router(members.my_studies_router)

# 일정
app.include_router(schedules.router)


# 서버 상태 확인
@app.get("/health", tags=["공통"])
def health():
    return {"status": "ok"}
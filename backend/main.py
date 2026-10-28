"""앱을 시작하고 각 담당자의 라우터를 연결하는 공통 파일입니다."""
from fastapi import FastAPI
from app.auth.routes import users
from app.studies.routes import studies, categories
from app.members.routes import members
from app.schedules.routes import schedules

app = FastAPI(title="스터디 관리 API")

# 라우터 틀만 연결했습니다. 각 API는 담당자가 해당 파일에서 구현합니다.
app.include_router(users.router)
app.include_router(studies.router)
app.include_router(categories.router)
app.include_router(members.router)
app.include_router(schedules.router)

@app.get("/health", tags=["공통"])
def health():
    """앱의 기본 상태 확인용 경로입니다."""
    return {"status": "ok"}

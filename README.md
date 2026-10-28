# 스터디 / 모임 관리 FastAPI 팀 프로젝트

이 ZIP은 팀원들이 직접 기능을 구현하기 위한 **시작용 뼈대**입니다. `GET /health`를 제외한 회원가입, 로그인, 스터디 CRUD, 참가, 일정 API와 DB 테이블은 아직 작성하지 않았습니다. 각 파일의 TODO를 참고해서 구현하세요.

## 파일 트리

```text
study-project-starter/
├── .gitignore
├── README.md
├── TEAM_WORK.md                 # 담당별 폴더와 작업 안내
└── backend/
    ├── .env.example             # 환경설정 예시
    ├── main.py                  # 앱과 라우터 연결
    ├── requirements.txt
    └── app/
        ├── core/
        │   ├── settings.py      # 환경설정
        │   └── security.py      # 인증 담당 구현 자리
        ├── db/
        │   ├── database.py      # ORM Base, DB 세션
        │   └── model_registry.py # ORM 모델 등록 자리
        ├── auth/                # 회원·인증
        │   ├── models/user.py
        │   ├── schemas/user.py
        │   └── routes/users.py
        ├── studies/             # 스터디·카테고리
        │   ├── models/study.py, category.py
        │   ├── schemas/study.py, category.py
        │   └── routes/studies.py, categories.py
        ├── members/             # 참가·취소
        │   ├── models/member.py
        │   ├── schemas/member.py
        │   └── routes/members.py
        └── schedules/           # 일정
            ├── models/schedule.py
            ├── schemas/schedule.py
            └── routes/schedules.py
```

폴더마다 `__init__.py`가 포함되어 있습니다. `models`는 DB 테이블, `schemas`는 요청·응답 검증, `routes`는 API 경로를 담당합니다.

## 실행 준비

Python 3.11 이상을 준비하고 압축을 푼 프로젝트 폴더에서 시작합니다.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cp .env.example .env
# Windows PowerShell: Copy-Item .env.example .env
python -m uvicorn main:app --reload
```

브라우저에서 `http://127.0.0.1:8000/docs`를 열면 공통 상태 확인 경로가 표시됩니다. 각 기능을 구현하고 라우터에 추가하면 해당 경로도 나타납니다. 이 ZIP은 요청에 따라 실행·테스트하지 않았습니다.

기본 DB 주소는 로컬 SQLite입니다. `.env`의 `DATABASE_URL`을 수정하면 MySQL로 바꿀 수 있습니다. MySQL 서버와 사용할 DB는 별도로 준비해야 합니다. 비밀번호에 특수문자가 있으면 URL 인코딩 등 접속 설정에 주의하세요. **테이블은 자동 생성되지 않습니다.** ORM 모델이 모두 준비되면 DB 담당자가 모델 등록·테이블 생성 또는 수업에서 사용하는 마이그레이션 방식을 연결하세요.

JWT 기능을 작성할 때는 `.env`에 각자 충분히 긴 임의의 `SECRET_KEY`를 넣고, 빈 키로 토큰을 발급하지 않도록 구현하세요. 실제 `.env`는 Git에 올리지 않습니다.

## Git 최초 등록

팀에서 만든 빈 원격 저장소의 주소를 확인한 뒤 압축을 푼 최상위 폴더에서 실행합니다.

```bash
git init -b main
git add .
git status
git commit -m "chore: add FastAPI project skeleton"
git remote add origin https://github.com/계정명/저장소명.git
git push -u origin main
```

주소는 실제 저장소로 바꾸고, `git status`에서 `.env`와 가상환경이 올라가지 않았는지 확인하세요. 기존 커밋이 있는 저장소에는 먼저 팀과 병합 방법을 협의하세요.

# 공통 DB 모델과 라우터 작업 안내

이 문서는 공통으로 준비한 프로젝트 구조와 팀원별 후속 작업을 정리한 안내입니다. 현재 시점의 기록은 2026년 10월 29일 확인한 상태이며, 이후 작업이 진행되면 담당자가 갱신해 주세요.

## 1. 현재 GitHub 상태

### GitHub `main`에 올라간 내용

- 첫 커밋 `2c4f485`: 프로젝트 폴더, 기본 DB 연결 코드, 빈 모델·스키마·라우터 파일, `.gitignore`, `.env.example`, `README.md`, `TEAM_WORK.md`.
- 커밋 `d26a102`: 공통 DB 모델, 모델 등록 코드, 기본 라우터 경로와 이 안내 문서를 추가했습니다.
- 커밋 `47dd3bc`: `StudyMember` 모델을 `models/member.py`로 옮겼습니다.
- 각 기능 라우터는 `501 구현 예정`을 반환하는 틀이며 실제 회원가입·로그인·CRUD 기능은 아직 구현되지 않았습니다.

### DB 모델 위치와 남은 확인

- `StudyMember` ORM 모델은 `backend/app/members/models/member.py`에 있으며 `model_registry.py`도 같은 위치에서 불러옵니다.
- `backend/app/members/schemas/member.py`는 현하 님이 참가 요청·응답용 Pydantic 스키마를 작성할 자리입니다.
- 5개 모델과 기본 라우터가 GitHub `main`에 올라가 있습니다. 실제 DB 연결·테이블 생성은 아직 검증되지 않았습니다.
- SQLite를 사용하는 경우 외래키 기능을 활성화해야 모델의 `ON DELETE CASCADE`가 적용됩니다. MySQL에서도 실제 DB 설정을 확인해야 합니다.

### 작업할 때 확인할 사항

1. 각 모델의 클래스명·컬럼명·외래키가 팀이 사용하는 테이블 정의서와 같은지 확인합니다.
2. SQLite 또는 MySQL에서 외래키와 테이블 생성 방식을 확인합니다.
3. `git status`로 올릴 파일을 확인하고 실제 `.env`나 비밀번호가 포함되지 않았는지 확인합니다.

## 2. 라우터는 어떻게 동작하나요?

```text
main.py
  └─ app.include_router(각 파일의 router)
       └─ routes/*.py에서 정한 HTTP 메서드와 주소를 앱에 연결
```

예를 들어 `studies.py`의 `router = APIRouter(prefix="/studies")`와 `@router.get("/{study_id}")`가 합쳐져 `GET /studies/{study_id}` 경로가 됩니다. `{study_id}`는 경로 매개변수입니다.

`main.py`에서 다음 라우터를 연결한 상태입니다.

| 라우터 | 기본 주소 | 역할 |
| --- | --- | --- |
| `users.router` | `/users` | 회원가입·내 정보 |
| `users.auth_router` | `/auth` | 로그인·토큰 |
| `studies.router` | `/studies` | 스터디 모집 |
| `categories.router` | `/categories` | 카테고리 |
| `members.router` | `/studies` | 참가·취소·참가자 |
| `members.my_studies_router` | `/users/me` | 내가 참가한 스터디 |
| `schedules.router` | `/studies` | 스터디 일정 |

여러 라우터가 같은 `/studies` 접두사를 사용할 수 있습니다. 다만 **같은 HTTP 메서드와 전체 경로를 중복 등록하지 않도록** 담당자끼리 경로를 확인해야 합니다.

## 3. 팀원이 지우고 구현할 부분

현재 각 함수는 경로의 자리를 보여주는 틀입니다. 기능을 구현할 때는 **`raise HTTPException(status_code=501, ...)` 부분을 실제 동작으로 바꿉니다.**

예를 들어 기존 코드가 다음과 같다면:

```python
@router.get("/{study_id}")
def read_study(study_id: int):
    raise HTTPException(
        status_code=501,
        detail="스터디 상세 조회 기능 구현 예정",
    )
```

담당자는 `raise HTTPException(...)`을 제거하고 스터디 조회·없는 경우의 오류 처리·응답을 구현합니다. `@router.get(...)`과 `study_id`는 경로를 정하는 부분이므로 기본적으로 유지하고, 필요한 DB 세션·Pydantic 입력/응답 모델·인증 의존성을 추가합니다. 합의에 따라 경로 자체를 바꿀 때는 관련 팀원과 명세도 함께 수정합니다.

`HTTPException`은 404·401·403 등 실제 오류 처리에도 쓰일 수 있으므로, **501 부분을 지운다고 import를 무조건 지우지는 않습니다.** 각 경로의 요청 Body·Query·응답 스키마와 인증 처리는 아직 작성되지 않았습니다.

## 4. 담당자별 경로와 작업 파일

### 아름 님 — 회원·인증

작업: `backend/app/auth/routes/users.py`, `backend/app/auth/schemas/`, `backend/app/core/security.py`

| 메서드 | 경로 | 구현할 기능 |
| --- | --- | --- |
| POST | `/users` | 회원가입 |
| GET | `/users/me` | 로그인 사용자 정보 조회 |
| POST | `/auth/token` | 로그인 및 JWT 발급 |

회원가입 입력·응답 스키마, 비밀번호 해싱, OAuth2 로그인 입력, JWT 발급·검증을 구현합니다. OAuth2 토큰 주소와 로그인 경로를 일치시키고 응답에 비밀번호 해시가 포함되지 않도록 합니다.

### 효정 님 — 스터디·카테고리·일정

작업: `backend/app/studies/routes/`, `backend/app/studies/schemas/`, `backend/app/schedules/routes/`, `backend/app/schedules/schemas/`

| 메서드 | 경로 | 구현할 기능 |
| --- | --- | --- |
| GET / POST | `/studies` | 스터디 목록·검색 / 생성 |
| GET / PUT / DELETE | `/studies/{study_id}` | 상세 / 수정 / 삭제 |
| GET | `/categories` | 카테고리 목록 |
| GET / POST | `/studies/{study_id}/schedules` | 일정 목록 / 등록 |
| PUT / DELETE | `/studies/{study_id}/schedules/{schedule_id}` | 일정 수정 / 삭제 |

스터디의 Query 검색, Pydantic 요청 Body와 응답, 스터디·일정 작성자 권한을 구현합니다. 일정 입력 시각과 시간대 규칙은 팀과 먼저 맞춥니다.

### 현하 님 — 참가·정원

작업: `backend/app/members/routes/members.py`, `backend/app/members/schemas/`

| 메서드 | 경로 | 구현할 기능 |
| --- | --- | --- |
| POST | `/studies/{study_id}/members` | 스터디 참가 |
| DELETE | `/studies/{study_id}/members/me` | 본인 참가 취소 |
| GET | `/studies/{study_id}/members` | 참가자 목록 |
| GET | `/users/me/studies` | 내가 참가한 스터디 목록 |

로그인 사용자 확인, 중복 참가 방지, 모집 상태·정원 확인을 구현합니다. 동시에 여러 요청이 오는 경우 정원을 보장할지는 재영 님과 범위·DB 처리 방식을 함께 결정합니다.

### 재영 님 — 공통 모델·통합

작업: 각 `models/`, `backend/app/db/`, `backend/main.py`, 공통 설정·Git.

5개 ORM 모델과 FK를 정리하고, API 경로와 공통 설정을 팀원들과 맞춥니다. 각자의 코드가 완성되면 `main.py` 연결과 DB 모델·스키마 이름을 확인합니다. 정원 처리 검토를 지원하고 팀원들이 작성한 API 명세와 실행 결과를 취합합니다.

## 5. 공통 DB와 협업 시 주의사항

- `models/`는 DB 테이블 구조, `schemas/`는 API 입력·응답 검증, `routes/`는 요청 경로와 처리 코드를 담당합니다.
- 모델 등록을 위해 `model_registry.py`가 모델을 import하는 것과 실제 DB에 테이블을 생성하는 것은 다른 작업입니다. 현재 코드에는 자동 테이블 생성이 없습니다.
- 현재 모델 기준 사용자 기본키는 `users.id`이고 비밀번호 해시 컬럼은 `hashed_password`입니다. 팀에서 이름을 바꾸기로 합의하면 FK·스키마·API를 함께 수정해야 합니다.
- `.env.example`은 설정 이름을 공유하는 예시이며, 실제 DB 비밀번호와 JWT 키가 담긴 `.env`는 Git에 올리지 않습니다.
- 각 기능 담당자는 본인의 API 명세와 정상·오류 처리를 함께 작성합니다. 공통 파일 수정은 관련 담당자와 조율합니다.

## 6. 팀원이 코드를 받는 시점

공통 모델과 기본 라우터는 GitHub `main`에 올라가 있으므로 팀원들이 저장소를 처음 복제하거나 최신 코드를 가져올 수 있습니다. 이미 저장소를 복제한 팀원은 현재 작업을 안전하게 저장한 뒤 최신 `main`을 가져오고, 자신의 작업 브랜치에 반영합니다.

이 파일은 작업 안내이며, GitHub 반영 여부는 실제 커밋·푸시와 GitHub 저장소에서 확인해야 합니다.

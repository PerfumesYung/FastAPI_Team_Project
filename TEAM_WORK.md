# 팀원별 작업 폴더 안내

## 확정된 역할분담

팀에서 확정한 역할을 기준으로 작업합니다. 공통 모델의 변경이나 기능 간 연결이 필요하면 관련 담당자와 먼저 조율합니다.

| 작업 | 담당자 이름 | 주로 수정할 위치 | 할 일 |
| --- | --- | --- | --- |
| 회원·인증 | 아름 님 | `backend/app/auth/routes/`, `backend/app/auth/schemas/`, `backend/app/core/security.py` | 회원가입·로그인·JWT·내 정보·인증 검증 |
| 스터디·카테고리 | 효정 님 | `backend/app/studies/routes/`, `backend/app/studies/schemas/` | 모집글 CRUD·검색·카테고리 |
| 참가·취소 | 현하 님 | `backend/app/members/routes/`, `backend/app/members/schemas/` | 참가·취소·목록·정원 확인 |
| 일정 | 효정 님 | `backend/app/schedules/routes/`, `backend/app/schedules/schemas/` | 일정 CRUD·권한 검증 |
| 공통 구조·DB | 재영 님 | 각 `backend/app/*/models/`, `backend/app/db/`, `backend/app/core/settings.py`, `backend/main.py` | 공통 ORM 모델, DB 설정, 모델 등록, 라우터 연결 |
| Git·통합·제출 | 재영 님 | `.gitignore`, `requirements.txt`, `README.md`, 공통 문서 | PR 조율·통합 확인·API 명세와 실행 결과 취합 |

효정 님이 스터디와 일정을 함께 담당하며, 일정 코드는 별도의 `schedules/` 폴더에서 작업합니다. 공통 ORM 모델은 재영 님이 먼저 작성했습니다. 사용자·스터디·참가 담당은 필요한 공통 항목과 FK를 함께 확인합니다.

## 폴더 안에서 무엇을 하나요?

- `models/`: 재영 님이 먼저 작성한 SQLAlchemy ORM 모델입니다. 테이블·컬럼·FK 변경이 필요하면 함께 조율합니다.
- `schemas/`: Pydantic 요청·응답 모델을 작성합니다. 비밀번호 해시 등 비밀 정보는 응답에서 제외합니다.
- `routes/`: FastAPI 경로를 작성합니다. 필요하면 `Depends(get_db)`로 DB 세션을 받습니다.
- 각 담당자는 본인 기능의 API 명세와 입력·오류 처리도 함께 준비합니다.

## 1. 아름 님 — 회원·인증

작업: `app/auth/schemas/user.py`, `app/auth/routes/users.py`, `app/core/security.py`. 공통 모델 `app/auth/models/user.py`는 재영 님과 조율합니다.

- 공통 `users` ORM 모델을 사용하고 회원가입 요청·응답 모델을 작성합니다.
- 비밀번호 해시, OAuth2 로그인, JWT 발급·검증, 현재 사용자 확인을 구현합니다.
- 로그인 경로와 OAuth2의 `tokenUrl`을 같게 맞추고, 빈 `SECRET_KEY`를 거부합니다.
- 다른 담당자가 사용할 로그인 사용자 의존성의 import 경로를 팀에 공유합니다.

## 2. 효정 님 — 스터디·카테고리

작업: `app/studies/schemas/`, `app/studies/routes/`. 공통 모델 변경은 재영 님과 조율합니다.

- 공통 `study_groups`, `study_categories` 모델을 사용하고 관련 Pydantic 모델을 작성합니다.
- 스터디 생성·조회·상세·수정·삭제, 검색과 카테고리 조회를 구현합니다.
- 상세 경로의 Path, 검색 Query, 생성·수정 Request Body를 명세에 적습니다.
- 작성자만 수정·삭제하도록 인증 담당과 의존성을 맞춥니다.

## 3. 현하 님 — 참가·취소

작업: `app/members/schemas/member.py`, `app/members/routes/members.py`. 공통 모델 변경은 재영 님과 조율합니다.

- 공통 `study_members` 모델을 사용하고 참가·취소·참가자 목록을 구현합니다.
- 중복 참가·모집 상태·정원 확인 규칙을 팀과 정합니다.
- 내 참가 목록은 `members.py`의 `my_studies_router`에 `/users/me/studies` 경로 틀이 이미 연결되어 있습니다. 인증 담당과 로그인 사용자 확인 방법을 맞춥니다.
- 정원 확인 후 참가하는 단순 구현은 동시에 여러 요청이 오면 초과할 수 있습니다. 동시 요청까지 다룰지 팀에서 범위를 결정하고 지원 담당을 정합니다.

## 4. 효정 님 — 일정

작업: `app/schedules/schemas/schedule.py`, `app/schedules/routes/schedules.py`. 공통 모델 변경은 재영 님과 조율합니다.

- 공통 `study_schedules` 모델을 사용하고 일정 등록·조회·수정·삭제 API를 작성합니다.
- 날짜·시간대 규칙은 팀과 합의합니다.
- `study_id` 외래키와 작성자 권한 확인 방법을 스터디·인증 담당과 맞춥니다.

## 5. 재영 님 — 공통 구조·DB

작업: `app/db/`, `app/core/settings.py`, `main.py`, `.env.example`, `requirements.txt`.

- 각 모델의 테이블명·PK·FK·자료형과 제약을 팀원과 함께 확인합니다.
- 공통 모델은 `app/db/model_registry.py`에 import되어 있습니다. 팀이 선택한 테이블 생성 방식을 연결합니다. **이 뼈대는 자동으로 테이블을 만들지 않습니다.**
- 모델 간 문자열 FK와 import 경로를 맞추고, 팀원이 새 라우터를 만들면 `main.py`에 등록합니다. 현재 기본 경로는 연결되어 있고 실제 기능은 `501 구현 예정` 상태입니다.
- `main.py`와 공통 설정을 여러 명이 동시에 수정해야 한다면 담당자와 먼저 조율합니다.

## Git 충돌 줄이는 약속

- `main`은 통합된 코드, 각 기능은 `feature/auth`, `feature/studies`, `feature/members`, `feature/integration` 등의 브랜치에서 작업합니다. 일정은 담당자에 맞게 브랜치를 정합니다.
- 각자 담당 폴더에서 작업하고 PR을 올립니다. 공동 파일은 지정된 담당자와 먼저 이야기합니다.
- 예: 일정 담당자는 `app/schedules/`를 수정하고 공통 설정이 필요하면 공통 담당자에게 요청합니다.
- PR에 변경 내용·동작 확인 결과·DB 변경 여부를 적고 다른 팀원이 확인한 후 병합합니다.
- 실제 `.env`는 공유하지 않고, 필요한 설정의 이름만 `.env.example`에 기록합니다.

## 제출 요구사항 확인

5~6개 테이블, Pydantic, Path·Query·Request Body, SQLAlchemy ORM/CRUD, OAuth와 JWT를 이용한 인증·권한, REST API 명세를 팀이 함께 구현합니다. 최종 경로 실행 결과는 Swagger UI 또는 Thunder Client/Postman으로 준비합니다.

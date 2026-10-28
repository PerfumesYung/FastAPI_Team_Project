# 팀원별 작업 폴더 안내

## 먼저 정할 것

아래 배정은 **예시**입니다. 팀원 네 분이 각자의 희망·가능한 시간과 난이도를 확인한 뒤 이름과 역할을 정합니다. 팀장 직책과 DB·Git 같은 공통 기술 작업 담당은 분리할 수 있습니다.

| 작업 | 담당자 이름 | 주로 수정할 위치 | 할 일 |
| --- | --- | --- | --- |
| 회원·인증 | 미정 | `backend/app/auth/`, `backend/app/core/security.py` | users 모델, 회원가입·로그인·JWT·내 정보 |
| 스터디·카테고리 | 미정 | `backend/app/studies/` | 모집글·카테고리 모델, CRUD, 검색 |
| 참가·취소 | 미정 | `backend/app/members/` | 참가 모델, 참가·취소·목록·정원 확인 |
| 일정 | 미정 | `backend/app/schedules/` | 일정 모델, 등록·조회 등 합의한 API |
| 공통 구조·DB | 미정 | `backend/app/db/`, `backend/app/core/settings.py`, `backend/main.py` | DB 설정, 모델 등록, 공통 라우터 조립 |
| Git·통합·제출 | 미정 | `.gitignore`, `requirements.txt`, `README.md`, 공통 문서 | PR 조율, 통합 확인, API 명세 취합 |

4명 팀이므로 한 사람이 여러 영역을 맡을 수 있습니다. **일정은 별도 폴더**로 두었으니 스터디 담당이나 희망하는 팀원이 맡을 수 있습니다. 공통 작업을 추가로 맡은 사람은 기능 범위를 함께 조정하세요. 사용자·스터디·참가 담당이 필요한 공통 항목과 FK를 먼저 맞춥니다.

## 폴더 안에서 무엇을 하나요?

- `models/`: SQLAlchemy ORM 클래스와 테이블·컬럼·FK를 작성합니다.
- `schemas/`: Pydantic 요청·응답 모델을 작성합니다. 비밀번호 해시 등 비밀 정보는 응답에서 제외합니다.
- `routes/`: FastAPI 경로를 작성합니다. 필요하면 `Depends(get_db)`로 DB 세션을 받습니다.
- 각 담당자는 본인 기능의 API 명세와 입력·오류 처리도 함께 준비합니다.

## 1. 회원·인증 담당

작업: `app/auth/models/user.py`, `app/auth/schemas/user.py`, `app/auth/routes/users.py`, `app/core/security.py`.

- `users` ORM 모델, 회원가입 요청·응답 모델을 작성합니다.
- 비밀번호 해시, OAuth2 로그인, JWT 발급·검증, 현재 사용자 확인을 구현합니다.
- 로그인 경로와 OAuth2의 `tokenUrl`을 같게 맞추고, 빈 `SECRET_KEY`를 거부합니다.
- 다른 담당자가 사용할 로그인 사용자 의존성의 import 경로를 팀에 공유합니다.

## 2. 스터디·카테고리 담당

작업: `app/studies/models/`, `app/studies/schemas/`, `app/studies/routes/`.

- `study_groups`, `study_categories` 모델과 관련 Pydantic 모델을 작성합니다.
- 스터디 생성·조회·상세·수정·삭제, 검색과 카테고리 조회를 구현합니다.
- 상세 경로의 Path, 검색 Query, 생성·수정 Request Body를 명세에 적습니다.
- 작성자만 수정·삭제하도록 인증 담당과 의존성을 맞춥니다.

## 3. 참가·취소 담당

작업: `app/members/models/member.py`, `app/members/schemas/member.py`, `app/members/routes/members.py`.

- `study_members` 모델과 참가·취소·참가자 목록을 작성합니다.
- 중복 참가·모집 상태·정원 확인 규칙을 팀과 정합니다.
- 내 참가 목록의 경로와 담당 파일은 인증 담당과 합의합니다. 현재 참가 라우터에는 `/studies` 접두사가 있으므로 `/users/me/studies` 경로를 만든다면 해당 접두사와 충돌하지 않도록 별도 라우터를 사용하고 공통 구조 담당자에게 등록을 요청하세요.
- 정원 확인 후 참가하는 단순 구현은 동시에 여러 요청이 오면 초과할 수 있습니다. 동시 요청까지 다룰지 팀에서 범위를 결정하고 지원 담당을 정합니다.

## 4. 일정 담당

작업: `app/schedules/models/schedule.py`, `app/schedules/schemas/schedule.py`, `app/schedules/routes/schedules.py`.

- `study_schedules` 모델과 일정 등록·조회 API를 작성합니다.
- 일정 수정·삭제와 날짜·시간대 규칙은 팀과 합의한 범위에 따라 추가합니다.
- `study_id` 외래키와 작성자 권한 확인 방법을 스터디·인증 담당과 맞춥니다.

## 5. 공통 구조·DB 담당

작업: `app/db/`, `app/core/settings.py`, `main.py`, `.env.example`, `requirements.txt`.

- 각 모델의 테이블명·PK·FK·자료형과 제약을 팀원과 함께 확인합니다.
- 각자 모델을 작성한 뒤 `app/db/model_registry.py`에서 import하고, 팀이 선택한 테이블 생성 또는 마이그레이션 방식을 연결합니다. **이 뼈대는 자동으로 테이블을 만들지 않습니다.**
- 모델 간 문자열 FK와 import 경로를 맞추고, 팀원이 새 라우터를 만들면 `main.py`에 등록합니다. 기존 빈 라우터는 이미 연결되어 있습니다.
- `main.py`와 공통 설정을 여러 명이 동시에 수정해야 한다면 담당자와 먼저 조율합니다.

## Git 충돌 줄이는 약속

- `main`은 통합된 코드, 각 기능은 `feature/auth`, `feature/studies`, `feature/members`, `feature/integration` 등의 브랜치에서 작업합니다. 일정은 담당자에 맞게 브랜치를 정합니다.
- 각자 담당 폴더에서 작업하고 PR을 올립니다. 공동 파일은 지정된 담당자와 먼저 이야기합니다.
- 예: 일정 담당자는 `app/schedules/`를 수정하고 공통 설정이 필요하면 공통 담당자에게 요청합니다.
- PR에 변경 내용·동작 확인 결과·DB 변경 여부를 적고 다른 팀원이 확인한 후 병합합니다.
- 실제 `.env`는 공유하지 않고, 필요한 설정의 이름만 `.env.example`에 기록합니다.

## 제출 요구사항 확인

5~6개 테이블, Pydantic, Path·Query·Request Body, SQLAlchemy ORM/CRUD, OAuth와 JWT를 이용한 인증·권한, REST API 명세를 팀이 함께 구현합니다. 최종 경로 실행 결과는 Swagger UI 또는 Thunder Client/Postman으로 준비합니다.

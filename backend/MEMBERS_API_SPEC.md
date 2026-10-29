# Members API 명세 — 스터디 참가·취소·목록

브랜치: `hyunha/feature/members`  
작업 파일: `backend/app/members/routes/members.py`, `backend/app/members/schemas/member.py`, `backend/app/members/services.py`

## 인증

4개 경로 모두 로그인한 사용자를 필요합니다.  
JWT 토큰 검증은 `app.core.security.get_current_user`가 완성되면 연결합니다.  
현재는 `app/members/temp_auth.py`의 임시 의존성(401/501)이 사용합니다.

## 1. 스터디 참가

- **메서드/경로**: `POST /studies/{study_id}/members`
- **인증**: 로그인 사용자 (JWT)
- **Path**: `study_id`
- **Request Body**: 없음 (사용자는 토큰으로 식별)

**요청 성공**

- 201 Created

```json
{
  "id": 1,
  "user_id": 1,
  "study_id": 1,
  "joined_at": "2026-10-29T02:47:15.510978"
}
```

**오류**

| 코드 | 조건 | detail |
| --- | --- | --- |
| 404 | 스터디 없음 | `스터디 {study_id}가 없습니다.` |
| 400 | 모집 마감(CLOSED) | `모집이 마감된 스터디입니다.` |
| 409 | 중복 참가 | `이미 참가한 스터디입니다.` |
| 409 | 정원 초과 | `정원이 가득 찼습니다.` |
| 409 | 동시 요청으로 유니크 제약 충돌 | `이미 참가한 스터디입니다.` |
| 401 | 로그인 안 된 상태 | 인증 의존성(아름 JWT) |

**동시 요청 처리**: 사전에 정원·중복을 확인한 뒤, insert 중 유니크 제약(`uq_study_members_user_study`)에 걸리면 rollback 후 409로 응답합니다. (동시 요청 범위 최종 결정은 재영과 조율)

## 2. 내 참가 취소

- **메서드/경로**: `DELETE /studies/{study_id}/members/me`
- **인증**: 로그인 사용자 (JWT)
- **Path**: `study_id`, `me`는 로그인한 본인

**요청 성공**

- 200 OK (참가 기록 응답)

```json
{
  "id": 1,
  "user_id": 1,
  "study_id": 1,
  "joined_at": "2026-10-29T02:47:15.510978"
}
```

**오류**

| 코드 | 조건 | detail |
| --- | --- | --- |
| 404 | 스터디 없음 | `스터디 {study_id}가 없습니다.` |
| 404 | 참가 기록 없음 | `참가한 스터디가 아닙니다.` |
| 401 | 로그인 안 된 상태 | 인증 의존성(아름 JWT) |

## 3. 스터디 참가자 목록

- **메서드/경로**: `GET /studies/{study_id}/members`
- **인증**: 없음 (조회 전용)
- **Path**: `study_id`

**요청 성공**

- 200 OK

```json
{
  "study_id": 1,
  "max_members": 2,
  "participants": [
    {"user_id": 1, "username": "alice", "joined_at": "2026-10-29T02:47:15.510978"}
  ]
}
```

`joined_at` 오름차순 정렬이며, 사용자 정보(hashed_password)는 응답하지 않습니다.

**오류**

| 코드 | 조건 | detail |
| --- | --- | --- |
| 404 | 스터디 없음 | `스터디 {study_id}가 없습니다.` |

## 4. 내가 참가한 스터디 목록

- **메서드/경로**: `GET /users/me/studies`
- **인증**: 로그인 사용자 (JWT)
- **Path/Body**: 없음

**요청 성공**

- 200 OK

```json
{
  "studies": [
    {"study_id": 1, "title": "python", "status": "OPEN", "max_members": 2, "joined_at": "2026-10-29T02:47:15.510978"}
  ]
}
```

`joined_at` 오름차순 정렬, 참가하지 않은 스터디는 빈 목록 응답합니다.

**오류**

| 코드 | 조건 | detail |
| --- | --- | --- |
| 401 | 로그인 안 된 상태 | 인증 의존성(아름 JWT) |

## 실행 결과 확인 방법

Swagger UI (`/docs`) 또는 `backend/test_members.py`(TestClient)로 검증했습니다.

- TestClient: 참가 201 → 중복 409 → 마감 스터디 400 → 참가자 목록 200(alice 표시) → 내 스터디 목록 200 → 취소 200 → 목록 비움 → 취소 재시도 404
- Swagger: 각 경로에 400·401·404·409 응답이 OpenAPI에 표기되어 있음
- 스터디 없음(404): 모든 조회·참가 경로에서 확인

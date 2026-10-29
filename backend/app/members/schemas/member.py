"""
참가 신청은 요청 Body가 없습니다.
study_id는 Path 매개변수, 사용자는 JWT 토큰(로그인 사용자 의존성)으로 식별합니다.

오류 정책:
- 401: 로그인하지 않은 상태
- 404: 스터디 또는 참가 기록이 없는 경우
- 409: 중복 참가 또는 정원 초과
- 400: 모집이 CLOSED인 스터디에 참가하려는 경우
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemberResponse(BaseModel):
    """참가 신청·취소 결과로 반환하는 참가 기록 응답입니다."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    study_id: int
    joined_at: datetime


class StudyParticipant(BaseModel):
    """참가자 목록 한 명 분. 비밀번호 해시는 응답에 포함하지 않습니다."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    joined_at: datetime


class MyStudy(BaseModel):
    """내가 참가한 스터디 한 개 분. 참가 기록과 스터디 정보를 합쳐 응답합니다."""

    model_config = ConfigDict(from_attributes=True)

    study_id: int
    title: str
    status: str
    max_members: int
    joined_at: datetime


class ParticipantListResponse(BaseModel):
    """GET /studies/{study_id}/members 응답입니다."""

    study_id: int
    max_members: int
    participants: list[StudyParticipant]


class MyStudyListResponse(BaseModel):
    """GET /users/me/studies 응답입니다."""

    studies: list[MyStudy]

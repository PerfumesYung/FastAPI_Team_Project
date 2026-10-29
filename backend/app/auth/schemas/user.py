from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    #누락되거나 잘못된 데이터가 유입되면 FastAPI 내부에서 자동으로 '422 Unprocessable Entity' 에러를 유발합니다.
    email: EmailStr = Field(..., description="로그인용 이메일 형식 (형식 오류 자동 검증)")
    username: str = Field(..., min_length=2, max_length=50, description="최소 2자 이상, 최대 50자 이하의 유저 명칭")
    password: str = Field(..., min_length=4, description="암호화 전 평문 비밀번호 (보안을 위해 최소 4자 이상 설정)")

class UserRead(BaseModel):
    #지침 준수: 응답 데이터에서 hashed_password 필드를 완벽히 누락시켜 보안 유출을 차단합니다.
    id: int
    email: EmailStr
    username: str
    role: str

    class Config:
        from_attributes = True  #SQLAlchemy DB 객체를 Pydantic 규격으로 자동 변환해주는 설정

class Token(BaseModel):
    #로그인 성공 시 발급하는 JWT 토큰 규격
    access_token: str
    token_type: str
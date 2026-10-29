from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Literal, Annotated

#스터디 생성
class StudyCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150) #1~150자
    description: str = Field(min_length=1) # 1자 이상
    max_members: int = Field(gt=1) #2명 이상
    category_id: int = Field(gt=0) #0 이상


#업데이트할 컬럼
class StudyUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=150) #1~150자
    description: str = Field(min_length=1) # 1자 이상
    max_members: int = Field(gt=1)
    status: Literal["OPEN", "CLOSED"]

    model_config = ConfigDict(str_strip_whitespace=True)

    

# 결과 응답 (모든 컬림 포함)
class StudyResponse(BaseModel):
    id: int
    owner_id: int  #작성자 id
    category_id: int
    title: str
    description: str
    max_members: int
    status: Literal["OPEN", "CLOSED"]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
"""
프로젝트에서 사용하는 DB 모델을 한곳에 모아 등록합니다.

각 모델이 같은 Base를 상속하므로,
이 파일에서 모델을 import하면 Base.metadata에 테이블 정보가 등록됩니다.

이 파일을 import하는 것만으로 실제 DB에 테이블이 생성되지는 않습니다.
"""

from app.auth.models.user import User

from app.studies.models.category import StudyCategory
from app.studies.models.study import StudyGroup

from app.members.models.member import StudyMember

from app.schedules.models.schedule import StudySchedule
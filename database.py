from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite 데이터베이스 파일 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"  # 하나로 통일

# 데이터베이스 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델을 위한 베이스 클래스
Base = declarative_base()

# 📝 이슈 테이블 모델
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    issue_number = Column(String, unique=True, index=True)
    issue_name = Column(String, index=True)
    issue_date = Column(Date)
    response_period = Column(String)
    category = Column(String)
    response_team = Column(String)
    government_officials = Column(String)
    business_impact = Column(String)
    kpi = Column(String)
    issue_end_date = Column(Date)
    stakeholders = Column(String)
    result_summary = Column(String)
    completion_status = Column(String)
    other_remarks = Column(String)
    updated_at = Column(Date)  # ✅ 수정일자 추가
    is_hidden = Column(Boolean, default=False)
    authorized_users = Column(String, nullable=True)  # ✅ 요거!

    # ✅ 세부 진행 사항과 관계 설정
    details = relationship("IssueDetail", back_populates="issue", cascade="all, delete")

# 📝 세부 진행 사항 테이블
class IssueDetail(Base):
    __tablename__ = "issue_details"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))  # 이슈 ID
    date = Column(Date, nullable=False)  # 진행 날짜
    content = Column(String, nullable=False)  # 진행 내용
    file_path = Column(String, nullable=True)  # ✅ 파일 경로 추가

    # ✅ Issue 테이블과 관계 설정
    issue = relationship("Issue", back_populates="details")

# 📝 검토 제안 테이블
class ReviewProposal(Base):
    __tablename__ = "review_proposals"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    content = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    goal = Column(String, nullable=False)

# 📝 법령 개정 현황 테이블
class LawUpdate(Base):
    __tablename__ = "law_updates"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    law_name = Column(String, nullable=False)
    proclamation_date = Column(Date, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # 파일 경로 필드 추가
    notice_date = Column(Date, nullable=True)

# ✅ 테이블 생성 (테이블이 없는 경우에만)


# 🧪 실무협의체 - 이화학
class Physicochemical(Base):
    __tablename__ = "physicochemical"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # JSON 문자열로 저장

# 🧪 실무협의체 - 약효약해
class Efficacy(Base):
    __tablename__ = "efficacy"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # JSON 문자열로 저장

# 🧪 실무협의체 -잔류성
class Residue(Base):
    __tablename__ = "residue"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # JSON 문자열로 저장

# 🧪 실무협의체 - 독성성
class Toxicity(Base):
    __tablename__ = "toxicity"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # JSON 문자열로 저장

class Supplement(Base):
    __tablename__ = "supplements"

    id = Column(Integer, primary_key=True, index=True)
    supplement_date = Column(Date, nullable=False)       # 보완날짜
    category = Column(String, nullable=False)             # 보완분야 (이화학, 약효약해 등)
    content = Column(String, nullable=False)              # 보완내용
    responder = Column(String, nullable=False)            # 대응주체 (각 회사, 공동(협회))
    file_path = Column(String, nullable=True)             # 관련자료 (JSON 배열 형태로 저장)

    response_method = Column(String, nullable=True)       # 대응방법(현황) - 사후 입력
    response_result = Column(String, nullable=True)       # 대응결과 - 사후 입력

Base.metadata.create_all(bind=engine)

class TestReview(Base):
    __tablename__ = "test_reviews"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    category = Column(String, nullable=False)         # 하작물/동작물
    field = Column(String, nullable=False)            # 살균제/살충제/...
    crop_name = Column(String, nullable=False)
    pest_name = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)  # 시험기관명 (기존: pesticide_name)
    review_type = Column(String, nullable=False)       # 검토구분 (기존: treatment_method)
    review_item = Column(String, nullable=True)
    review_result = Column(String, nullable=True)

# ✅ DB 세션 주입용 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)  # 시작일
    end_date = Column(Date, nullable=True)     # 종료일 (없으면 단일일정)
    title = Column(String, nullable=False)     # 내용
    location = Column(String, nullable=True)   # 장소
    created_at = Column(DateTime, default=datetime.utcnow)

class ScheduleHistory(Base):
    __tablename__ = "schedule_history"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    title = Column(String)
    location = Column(String)
    deleted_at = Column(DateTime, default=datetime.utcnow)  # 삭제된 시점 기록

class LoginLog(Base):
    __tablename__ = "login_logs"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean)

class ActionLog(Base):
    __tablename__ = "action_logs"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    action_type = Column(String)  # 예: 'delete', 'update'
    target_table = Column(String)
    target_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class IssueAlertSubscription(Base):
    __tablename__ = "issue_alert_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
from app.repos.base_repo import BaseRepo
from sqlalchemy import Column, Integer, String, DateTime

from app.repos.base import Base

class Logs(Base):
    __tablename__ = "t_logs"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "comment": "로그 정보"
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="고유 PK")
    status = Column(String(200), nullable=False, comment="상태")
    message = Column(String(200), nullable=False, comment="메시지")
    data = Column(String(200), nullable=False, comment="데이터")
    username = Column(String(200), nullable=False, comment="사용자ID")
    trace_id = Column(String(100), nullable=False, comment="트레이스 ID")
    created_at = Column(DateTime, nullable=False, comment="생성일시")

class LogsRepo(BaseRepo):
    @property
    def table(self):
        return Logs.__table__

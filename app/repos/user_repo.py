from sqlalchemy import Column, Integer, String, Date, DateTime, text
from app.repos.base import Base, BaseRepo

class User(Base):
    __tablename__ = "t_user"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "comment": "회원 기본정보"
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="고유 PK")
    username = Column(String(50), nullable=False, unique=True, index=True, comment="아이디")
    password = Column(String(200), nullable=False, comment="비밀번호")
    created_at = Column(DateTime, comment="생성일시")
    updated_at = Column(DateTime, comment="수정일시")
    is_deleted = Column(String(1), server_default=text("'F'"), comment="삭제 여부")

class UserRepo(BaseRepo):
    @property
    def table(self):
        return User.__table__

    async def get_by_username(self, username: str):
        query = self.table.select().where(self.table.c.username == username)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None

from sqlalchemy import Table, MetaData, Column, String, Integer, Date, DateTime, text
from app.repos.base_repo import BaseRepo

table = Table(
    "t_user",
    MetaData(),
    Column("id", Integer, primary_key=True, autoincrement=True, comment="고유 PK"),
    Column("username", String(50), nullable=False, unique=True, index=True, comment="아이디"),
    Column("password", String(200), nullable=False, comment="비밀번호"),
    Column("created_at", DateTime, comment="생성일시"),
    Column("updated_at", DateTime, comment="수정일시"),
    Column("is_deleted", String(1), server_default=text("F"), comment="삭제 여부"),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    comment="회원 정보"
)


class UserRepo(BaseRepo):
    @property
    def table(self):
        return table

    async def get_by_username(self, username: str):
        query = self.table.select().where(self.table.c.username == username)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None

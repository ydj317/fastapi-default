from app.repos.base_repo import BaseRepo
import sqlalchemy

table = sqlalchemy.Table(
    "t_logs",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("status", sqlalchemy.String(length=10)),
    sqlalchemy.Column("message", sqlalchemy.String(length=255)),
    sqlalchemy.Column("data", sqlalchemy.Text),
    sqlalchemy.Column("username", sqlalchemy.String(length=200)),
    sqlalchemy.Column("trace_id", sqlalchemy.String(length=100)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
)


class LogsRepo(BaseRepo):
    @property
    def table(self):
        return table

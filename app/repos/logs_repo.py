from app.repos.base_repo import BaseRepo
import sqlalchemy

table = sqlalchemy.Table(
    "t_logs",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("status", sqlalchemy.String(length=10)),
    sqlalchemy.Column("message", sqlalchemy.String(length=255)),
    sqlalchemy.Column("data", sqlalchemy.Text),
    sqlalchemy.Column("trace_id", sqlalchemy.String(length=100)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
)

class LogsRepo(BaseRepo):
    @property
    def table(self):
        return table


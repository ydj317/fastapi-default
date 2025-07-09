import sqlalchemy
from app.repositories.base_repo import BaseRepo

table = sqlalchemy.Table(
    "t_user",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

class UserRepo(BaseRepo):
    @property
    def table(self):
        return table

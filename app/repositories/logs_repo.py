from datetime import datetime
from databases import Database
import sqlalchemy

metadata = sqlalchemy.MetaData()

t_logs = sqlalchemy.Table(
    "t_logs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("status", sqlalchemy.String(length=10)),
    sqlalchemy.Column("message", sqlalchemy.String(length=255)),
    sqlalchemy.Column("data", sqlalchemy.Text),
    sqlalchemy.Column("trace_id", sqlalchemy.String(length=100)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
)

class LogsRepo:
    def __init__(self, db: Database):
        self.db = db

    async def insert(self, status: str, message: str, data: str, trace_id: str):
        query = t_logs.insert().values(
            status=status,
            message=message,
            data=data,
            trace_id=trace_id,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return await self.db.execute(query)


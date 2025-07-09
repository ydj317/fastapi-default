from app.repos.logs_repo import LogsRepo
from app.core.context import get_trace_id

class Logs:

    logs_repo: LogsRepo

    @classmethod
    def init(cls, logs_repo: LogsRepo):
        cls.logs_repo = logs_repo

    @classmethod
    async def write(cls, status: str = "INFO", message: str = "", data=None):
        print(cls.logs_repo)
        await cls.logs_repo.create(status=status, message=message, data=data, trace_id=get_trace_id())

    @classmethod
    async def debug(cls, message: str, data: any):
        await cls.write(status='DEBUG', message=message, data=data)

    @classmethod
    async def info(cls, message: str, data: any):
        await cls.write(status='INFO', message=message, data=data)

    @classmethod
    async def error(cls, message: str, data: any):
        await cls.write(status='ERROR', message=message, data=data)
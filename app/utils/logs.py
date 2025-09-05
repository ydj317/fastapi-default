from app.repos.logs_repo import LogsRepo
from app.core.context import get_trace_id, get_username
import json

def to_json(data) -> str:
    try:
        if isinstance(data, str):
            data = {"text": data}

        return json.dumps(
            data,
            ensure_ascii=False,               # 한글 깨짐 방지
            default=lambda o: o.__dict__      # 일반 객체 → dict 변환
        )
    except TypeError as e:
        return ""

class Logs:

    logs_repo: LogsRepo

    @classmethod
    def init(cls, logs_repo: LogsRepo):
        cls.logs_repo = logs_repo

    @classmethod
    async def write(cls, status: str = "INFO", message: str = "", data=None):
        data = to_json(data)
        await cls.logs_repo.create(
            status=status,
            message=message,
            data=data,
            username=get_username(),
            trace_id=get_trace_id()
        )

    @classmethod
    async def debug(cls, message: str, data: any):
        await cls.write(status='DEBUG', message=message, data=data)

    @classmethod
    async def info(cls, message: str, data: any):
        await cls.write(status='INFO', message=message, data=data)

    @classmethod
    async def error(cls, message: str, data: any):
        await cls.write(status='ERROR', message=message, data=data)
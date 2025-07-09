from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
import redis.asyncio as redis

from app.celery_worker import my_task
from app.core.settings import settings
from redis.asyncio import Redis
from app.core.containers import Container
from app.tasks.my_task import add
from celery.result import AsyncResult

router = APIRouter()

@router.get("/test/exception")
def rase_exception():
    raise Exception('rase exception!!!')

@router.get("/test/task/add")
def run_add_task(a: int, b: int):
    result = add.delay(a, b)
    return {"task_id": result.id}

@router.get("/test/task/result/{task_id}")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=my_task)

    if result.state == "PENDING":
        return {"status": "PENDING"}

    elif result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": result.result}

    elif result.state == "FAILURE":
        return {"status": "FAILURE", "error": str(result.result)}

    else:
        return {"status": result.state}

@router.get("/test/redis")
@inject
async def test_redis(redis: Redis = Depends(Provide[Container.redis])):
    await redis.set("key", "value111")
    val = await redis.get("key")
    return {"key": val}

import redis.asyncio as redis
from typing import AsyncGenerator


async def get_redis(url: str) -> AsyncGenerator[redis.Redis, None]:
    client = redis.from_url(url, decode_responses=True)
    try:
        print("✅ Redis connected")
        yield client
    finally:
        await client.close()
        print("🔌 Redis disconnected")
import redis.asyncio as redis

async def get_redis(url: str) -> redis.Redis:
    return redis.from_url(url, decode_responses=True)
import asyncio
import json
from aio_pika import connect_robust, Message
from app.core.settings import settings

RABBITMQ_URL = settings.rabbitmq_url
QUEUE_NAME = "TEST_QUEUE"

async def publish():
    conn = await connect_robust(RABBITMQ_URL)
    channel = await conn.channel()

    await channel.declare_queue(QUEUE_NAME, durable=True)

    message = {
        "event": "user.created",
        "payload": {"user_id": 123, "name": "Alice"}
    }

    await channel.default_exchange.publish(
        Message(body=json.dumps(message).encode()),
        routing_key=QUEUE_NAME
    )

    print("✅ 메시지 발송 완료")

    # ✅ 연결 종료 (clean shutdown)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(publish())

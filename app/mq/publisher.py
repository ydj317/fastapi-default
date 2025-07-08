import asyncio
import json
from aio_pika import connect_robust, Message
from app.core.settings import settings

RABBITMQ_URL = settings.rabbitmq_url

async def publish(queue_name: str, message: str):
    conn = await connect_robust(RABBITMQ_URL)
    channel = await conn.channel()

    await channel.declare_queue(queue_name, durable=True)

    await channel.default_exchange.publish(
        Message(body=message.encode()),
        routing_key=queue_name
    )

    print("✅ 메시지 발송 완료")

    # ✅ 연결 종료 (clean shutdown)
    await conn.close()

if __name__ == "__main__":
    test_queue_name = 'TEST_QUEUE'
    test_message = json.dumps({
        "event": "user.created",
        "payload": {"user_id": 123, "name": "Alice"}
    })
    asyncio.run(publish(test_queue_name, test_message))

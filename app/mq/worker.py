import asyncio
import json
from aio_pika import IncomingMessage, connect_robust
from app.core.settings import settings

RABBITMQ_URL = settings.rabbitmq_url
QUEUE_NAME = "TEST_QUEUE"

async def handle_message(message: IncomingMessage):
    async with message.process():  # ✅ 자동 ack 처리
        try:
            data = json.loads(message.body.decode())
            print(f"📨 메시지 수신: {data}")
        except Exception as e:
            print(f"❌ 처리 실패: {e}")


async def main():
    # ✅ 연결 및 채널 열기
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    # ✅ 큐 선언 (Exchange 없이 직접)
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    # ✅ 메시지 consume
    print("🎯 메시지 수신 대기 중... (Ctrl+C to stop)")
    await queue.consume(handle_message)

    # ✅ graceful shutdown을 위한 무한 대기
    try:
        await asyncio.Future()  # Ctrl+C까지 대기
    finally:
        print("🛑 연결 종료 중...")
        await connection.close()
        print("✅ 연결 종료")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 종료 요청됨")

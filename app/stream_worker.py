from app.core.containers import Container
from app.core.stream import stream_app, broker, events_queue
from faststream.exceptions import NackMessage, RejectMessage
from app.core.settings import settings

# 실행 방법
# faststream run app.stream_worker:stream_app

container = Container()
container.config.from_dict(settings.dict())

async def on_startup():
    await container.init_resources()

async def on_shutdown():
    await container.shutdown_resources()

stream_app.on_startup(on_startup)
stream_app.on_shutdown(on_shutdown)

@broker.subscriber(events_queue)
async def consume_event(msg: dict):
    try:
        print(f"[Worker] Received: {msg}")

        if "error" in msg:
            raise ValueError("에러 발생!")

        # 정상 처리 → 자동 Ack
        return {"status": "ok"}

    except ValueError as e:
        print(f"[Worker] 처리 실패: {e}")

        # 재시도 횟수 확인 (RabbitMQ x-death 헤더 참고 가능)
        if msg.get("retry_count", 0) >= 3:
            # 3회 이상 실패 → DLQ
            raise RejectMessage()
        else:
            # 재시도
            raise NackMessage(requeue=True)

    except Exception as e:
        print(f"[Worker] 치명적 오류: {e}")
        # DLQ로 바로 보냄
        raise RejectMessage()

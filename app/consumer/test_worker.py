from app.core.context import set_trace_id
from app.consumer.stream import broker, test_queue
from faststream.exceptions import NackMessage, RejectMessage
from app.utils.logs import Logs


@broker.subscriber(test_queue)
async def consume_event(msg: dict):
    if "trace_id" in msg:
        set_trace_id(msg["trace_id"])

    await Logs.info(f"[Worker] Received: {msg}", f"[Worker] Received: {msg}")

    print(f"[Worker] Received: {msg}")

    if "error" in msg:
        raise ValueError("에러 발생!")

    return {"status": "ok"}

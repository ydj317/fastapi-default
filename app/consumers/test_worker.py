from app.core.context import set_trace_id
from app.consumers.stream import broker, test_queue
from faststream.exceptions import NackMessage, RejectMessage
from app.utils.logs import Logs


@broker.subscriber(test_queue)
async def consume_event(msg: dict):
    if "trace_id" in msg:
        set_trace_id(msg["trace_id"])

    await Logs.info(f"[Worker] test", msg)

    print(f"[Worker] Received: {msg}")

    return {"status": "ok"}

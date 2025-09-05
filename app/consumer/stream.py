from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from app.core.settings import settings

broker = RabbitBroker(settings.rabbitmq_url)
stream_app = FastStream(broker)

test_queue = RabbitQueue("test", durable=True, auto_delete=False)
async def publish_test_queue(data):
    await broker.publish(data, queue=test_queue)

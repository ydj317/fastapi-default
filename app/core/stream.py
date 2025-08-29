from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from app.core.settings import settings

broker = RabbitBroker(settings.rabbitmq_url)

events_queue = RabbitQueue("TEST_events", durable=True, auto_delete=False)

stream_app = FastStream(broker)

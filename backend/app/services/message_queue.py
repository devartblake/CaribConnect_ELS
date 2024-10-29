import asyncio
import logging
import aio_pika
from app.core.config import settings

logger = logging.getLogger(__name__)

async def get_connection():
    try:
        return await aio_pika.connect_robust(settings.RABBITMQ_URL)
    except Exception as e:
        logger.error(f"Error connecting to RabbitMQ: {e}")
        return None

async def send_message_async(queue_name: str, message_body: str):
    connection = await get_connection()
    if connection is None:
        logger.error("Connection to RabbitMQ failed, message not sent.")
        return

    async with connection:
        try:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()), routing_key=queue.name
            )
            logger.info(f"Message sent to queue '{queue_name}' with body: {message_body}")
        except Exception as e:
            logger.error(f"Error sending message to queue '{queue_name}': {e}")

def send_message(queue_name: str, message_body: str):
    asyncio.run(send_message_async(queue_name, message_body))

async def setup_rabbitmq():
    """Initialize RabbitMQ connection, channel, and queue."""
    connection = await get_connection()
    if connection is None:
        logger.error("Failed to initialize RabbitMQ connection.")
        return None, None, None

    async with connection:
        try:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            exchange = await channel.declare_exchange("my_exchange", aio_pika.ExchangeType.DIRECT)
            queue = await channel.declare_queue("my_queue", durable=True)
            await queue.bind(exchange, routing_key="test")
            logger.info("RabbitMQ setup complete.")
            return connection, channel, queue
        except Exception as e:
            logger.error(f"Error setting up RabbitMQ: {e}")
            return None, None, None

async def consume_from_stream(queue):
    async def message_handler(message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                logger.info(f"Received message: {message.body.decode()}")
                await process_message(message.body.decode())
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    await queue.consume(message_handler, no_ack=False)

async def process_message(message_body):
    """Process message and perform desired task."""
    logger.info(f"Processing message: {message_body}")
    # Add custom logic based on message contents

async def publish_message(channel, message_body):
    try:
        exchange = await channel.get_exchange("my_exchange")
        message = aio_pika.Message(body=message_body.encode())
        await exchange.publish(message, routing_key="test")
        logger.info(f"Published message: {message_body}")
    except Exception as e:
        logger.error(f"Error publishing message: {e}")

async def main():
    connection, channel, queue = await setup_rabbitmq()
    if not queue:
        logger.error("RabbitMQ setup failed, exiting.")
        return

    consumer_task = asyncio.create_task(consume_from_stream(queue))

    try:
        await publish_message(channel, "Hello, RabbitMQ with aio-pika!")
    except Exception as e:
        logger.error(f"Error in main function: {e}")

    await consumer_task  # Start consumer indefinitely

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service interrupted, shutting down.")

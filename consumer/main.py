import ast
import asyncio
import os
import aio_pika


from consumer.consumer import consume
from consumer.schema import ConsumerMessage


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        body = message.body
        body = body.decode("UTF-8")
        body = ast.literal_eval(body)
        await consume(ConsumerMessage(**body))


async def main() -> None:
    connection = await aio_pika.connect_robust(
        os.getenv("AMQP_URL"),
    )

    queue_name = "message"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name)

    await queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())

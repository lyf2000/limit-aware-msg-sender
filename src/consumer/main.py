import ast
import asyncio
import os
import aio_pika


from consumer.consume import consume
from consumer.schema import ConsumerMessage


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        body = message.body
        body = body.decode("UTF-8")
        body = ast.literal_eval(body)
        await consume(ConsumerMessage(**body))


def main(queue_num=1) -> None:
    asyncio.run((decl_xc()))
    asyncio.run(run_single_queue(queue_num))

    # queues_per_core = settings.QUEUE_N // multiprocessing.cpu_count()
    # if not queues_per_core:
    #     queues_per_core = 1

    # for queue_nums in chunker(range(settings.QUEUE_N), queues_per_core):
    #     multiprocessing.Process(target=run_queues_per_core, args=(queue_nums,)).start()


# def run_queues_per_core(nums: list[int]):
#     for queue_num in nums:
#         asyncio.run(run_single_queue(queue_num + 1))


async def decl_xc():
    connection = await aio_pika.connect_robust(os.getenv("AMQP_URL"))
    channel = await connection.channel()
    await channel.declare_exchange(
        "messages",
        aio_pika.ExchangeType.X_CONSISTENT_HASH,
        durable=True,
        auto_delete=False,
    )


async def run_single_queue(num: int) -> None:
    connection = await aio_pika.connect_robust(os.getenv("AMQP_URL"))

    queue_name = f"send_{num}"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name)
    await queue.bind(exchange="messages", routing_key=f"{num}")  # TODO why

    await queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    main()

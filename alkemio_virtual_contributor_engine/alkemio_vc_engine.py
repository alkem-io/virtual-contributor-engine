import asyncio
import json
from collections.abc import Callable, Coroutine
from typing import Any

from aio_pika.abc import AbstractIncomingMessage

from alkemio_virtual_contributor_engine.events import (
    Input,
    IngestWebsite,
    Response,
    IngestWebsiteResult,
)
from alkemio_virtual_contributor_engine.rabbitmq import RabbitMQ
from alkemio_virtual_contributor_engine.setup_logger import setup_logger


logger = setup_logger(__name__)


class AlkemioVirtualContributorEngine:

    def __init__(self):
        self.rabbitmq = RabbitMQ()
        self.handler = None

    async def start(self):
        await self.rabbitmq.connect()
        if self.handler is None:
            raise ValueError(
                "Message handler not defined. Ensure `engine.register_handler` with argument signature handler: `Callable[[Input], Coroutine[Any, Any, Response]]`  is called"
            )
        await self.rabbitmq.consume(self.invoke_handler)
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Engine shutdown initiated")
        except Exception as e:
            logger.error(f"Unexpected error in engine: {e}", exc_info=True)
            raise

    async def publish(self, queue, message):
        await self.rabbitmq.publish_to_queue(queue, message)

    async def consume(self, queue, callback, auto_delete=False, durable=True):
        await self.rabbitmq.consume_queue(queue, callback, auto_delete, durable)

    async def invoke_handler(self, message: AbstractIncomingMessage):
        logger.info("New message received.")
        if self.handler is None:
            raise ValueError(
                "Message handler not defined. Ensure `engine.register_handler` with argument signature handler: `Callable[[Input], Coroutine[Any, Any, Response]]`  is called"
            )

        async with message.process():
            try:
                body = json.loads(message.body.decode())
                event_type = body.get("eventType")
                if event_type == "IngestWebsite":
                    input = IngestWebsite(**body)
                else:
                    input = Input(**body["input"])

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message: {e}")
                return
            except KeyError as e:
                logger.exception(f"Missing required field: {e}")
                return

            response: Response | IngestWebsiteResult = await self.handler(input)

            result_message = {
                "response": response.dict(),
                "original": input.dict(),
            }
            logger.info("Handler completed.")
            try:
                await self.rabbitmq.publish(result_message)
            except Exception as e:
                logger.error(e)

            logger.debug(f"Result published: {result_message}.")
            logger.info("Response published.")

    def register_handler(
        self,
        # the handler type should be as follows
        # handler: Callable[[Input | IngestWebsite], Coroutine[Any, Any, Response]],
        # for some reason it's not working hence the Any there -.-
        handler: Callable[[Any], Coroutine[Any, Any, Response | IngestWebsiteResult]],
    ):
        self.handler = handler

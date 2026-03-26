import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from alkemio_virtual_contributor_engine.events import (
    Input,
    Response,
    IngestWebsite,
    IngestWebsiteResult,
)


@pytest.fixture
def engine():
    with patch(
        "alkemio_virtual_contributor_engine.alkemio_vc_engine.setup_logger"
    ) as mock_logger:
        mock_logger.return_value = MagicMock()
        with patch(
            "alkemio_virtual_contributor_engine.alkemio_vc_engine.RabbitMQ"
        ) as mock_rmq_cls:
            mock_rmq_cls.return_value = AsyncMock()
            from alkemio_virtual_contributor_engine.alkemio_vc_engine import (
                AlkemioVirtualContributorEngine,
            )
            eng = AlkemioVirtualContributorEngine()
    return eng


def test_register_handler(engine):
    handler = AsyncMock()
    engine.register_handler(handler)
    assert engine.handler is handler


@pytest.mark.asyncio
async def test_invoke_handler_query(engine):
    handler = AsyncMock(return_value=Response(result="ok"))
    engine.register_handler(handler)

    input_data = {
        "input": {
            "engine": "test-engine",
            "userID": "user-1",
            "message": "hello",
            "history": [{"content": "hi", "role": "human"}],
            "displayName": "Test",
            "personaID": "persona-1",
            "resultHandler": {"action": "postReply"},
        }
    }

    message = AsyncMock()
    message.body = json.dumps(input_data).encode()
    message.process = MagicMock()
    message.process.return_value.__aenter__ = AsyncMock()
    message.process.return_value.__aexit__ = AsyncMock(return_value=False)

    await engine.invoke_handler(message)
    handler.assert_awaited_once()
    arg = handler.call_args[0][0]
    assert isinstance(arg, Input)
    assert arg.message == "hello"


@pytest.mark.asyncio
async def test_invoke_handler_ingest(engine):
    handler = AsyncMock(return_value=IngestWebsiteResult())
    engine.register_handler(handler)

    ingest_data = {
        "eventType": "IngestWebsite",
        "baseUrl": "https://example.com",
        "type": "website",
        "purpose": "test",
        "personaId": "persona-1",
    }

    message = AsyncMock()
    message.body = json.dumps(ingest_data).encode()
    message.process = MagicMock()
    message.process.return_value.__aenter__ = AsyncMock()
    message.process.return_value.__aexit__ = AsyncMock(return_value=False)

    await engine.invoke_handler(message)
    handler.assert_awaited_once()
    arg = handler.call_args[0][0]
    assert isinstance(arg, IngestWebsite)


@pytest.mark.asyncio
async def test_invoke_handler_bad_json(engine):
    handler = AsyncMock()
    engine.register_handler(handler)

    message = AsyncMock()
    message.body = b"not json"
    message.process = MagicMock()
    message.process.return_value.__aenter__ = AsyncMock()
    message.process.return_value.__aexit__ = AsyncMock(return_value=False)

    await engine.invoke_handler(message)
    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_invoke_handler_missing_field(engine):
    handler = AsyncMock()
    engine.register_handler(handler)

    message = AsyncMock()
    message.body = json.dumps({"some": "data"}).encode()
    message.process = MagicMock()
    message.process.return_value.__aenter__ = AsyncMock()
    message.process.return_value.__aexit__ = AsyncMock(return_value=False)

    await engine.invoke_handler(message)
    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_invoke_handler_no_handler(engine):
    message = AsyncMock()
    message.body = json.dumps({"input": {}}).encode()
    message.process = MagicMock()
    message.process.return_value.__aenter__ = AsyncMock()
    message.process.return_value.__aexit__ = AsyncMock(return_value=False)

    with pytest.raises(ValueError, match="Message handler not defined"):
        await engine.invoke_handler(message)


@pytest.mark.asyncio
async def test_publish(engine):
    await engine.publish("queue", {"msg": "test"})
    engine.rabbitmq.publish_to_queue.assert_awaited_once()


@pytest.mark.asyncio
async def test_consume(engine):
    callback = AsyncMock()
    await engine.consume("queue", callback)
    engine.rabbitmq.consume_queue.assert_awaited_once()

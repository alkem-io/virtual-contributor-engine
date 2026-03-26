import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from alkemio_virtual_contributor_engine.rabbitmq import RabbitMQ


@pytest.fixture
def rabbitmq():
    with patch(
        "alkemio_virtual_contributor_engine.rabbitmq.setup_logger"
    ) as mock_logger:
        mock_logger.return_value = MagicMock()
        rmq = RabbitMQ()
    return rmq


@pytest.mark.asyncio
async def test_connect(rabbitmq):
    mock_conn = AsyncMock()
    mock_channel = AsyncMock()
    mock_queue = MagicMock()
    mock_exchange = MagicMock()

    mock_conn.channel = AsyncMock(return_value=mock_channel)
    mock_channel.declare_queue = AsyncMock(return_value=mock_queue)
    mock_channel.declare_exchange = AsyncMock(return_value=mock_exchange)
    mock_channel.set_qos = AsyncMock()
    mock_queue.bind = AsyncMock()

    with patch(
        "alkemio_virtual_contributor_engine.rabbitmq.connect_robust",
        AsyncMock(return_value=mock_conn),
    ):
        await rabbitmq.connect()

    assert rabbitmq.connection is mock_conn
    assert rabbitmq.channel is mock_channel
    assert rabbitmq.input_queue is not None
    assert rabbitmq.exchange is not None
    mock_channel.set_qos.assert_awaited_once_with(prefetch_count=1)


@pytest.mark.asyncio
async def test_consume(rabbitmq):
    mock_queue = AsyncMock()
    rabbitmq.input_queue = mock_queue
    callback = AsyncMock()

    await rabbitmq.consume(callback)
    mock_queue.consume.assert_awaited_once_with(callback)


@pytest.mark.asyncio
async def test_consume_no_queue(rabbitmq):
    rabbitmq.input_queue = None
    callback = AsyncMock()
    await rabbitmq.consume(callback)


@pytest.mark.asyncio
async def test_publish(rabbitmq):
    mock_exchange = AsyncMock()
    mock_channel = MagicMock()
    mock_channel.is_closed = False
    rabbitmq.exchange = mock_exchange
    rabbitmq.channel = mock_channel

    message = {"key": "value"}
    await rabbitmq.publish(message)
    mock_exchange.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_channel_closed_reopens(rabbitmq):
    mock_exchange = AsyncMock()
    mock_channel = AsyncMock()
    mock_channel.is_closed = True
    rabbitmq.exchange = mock_exchange
    rabbitmq.channel = mock_channel

    await rabbitmq.publish({"key": "value"})
    mock_channel.reopen.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_no_exchange(rabbitmq):
    rabbitmq.exchange = None
    rabbitmq.channel = MagicMock()
    rabbitmq.channel.is_closed = False
    await rabbitmq.publish({"key": "value"})


@pytest.mark.asyncio
async def test_consume_queue(rabbitmq):
    mock_channel = AsyncMock()
    mock_queue_obj = AsyncMock()
    mock_channel.declare_queue = AsyncMock(return_value=mock_queue_obj)
    rabbitmq.channel = mock_channel

    callback = AsyncMock()
    await rabbitmq.consume_queue("test-queue", callback)
    mock_queue_obj.consume.assert_awaited_once_with(callback)


@pytest.mark.asyncio
async def test_consume_queue_no_channel(rabbitmq):
    rabbitmq.channel = None
    callback = AsyncMock()
    await rabbitmq.consume_queue("test-queue", callback)


@pytest.mark.asyncio
async def test_publish_to_queue(rabbitmq):
    mock_channel = AsyncMock()
    mock_channel.is_closed = False
    mock_default_exchange = AsyncMock()
    mock_channel.default_exchange = mock_default_exchange
    rabbitmq.channel = mock_channel

    await rabbitmq.publish_to_queue("test-queue", {"key": "value"})
    mock_default_exchange.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_publish_to_queue_no_channel(rabbitmq):
    rabbitmq.channel = None
    await rabbitmq.publish_to_queue("test-queue", {"key": "value"})


@pytest.mark.asyncio
async def test_publish_to_queue_channel_closed(rabbitmq):
    mock_channel = AsyncMock()
    mock_channel.is_closed = True
    mock_default_exchange = AsyncMock()
    mock_channel.default_exchange = mock_default_exchange
    rabbitmq.channel = mock_channel

    await rabbitmq.publish_to_queue("test-queue", {"key": "value"})
    mock_channel.reopen.assert_awaited_once()


@pytest.mark.asyncio
async def test_connect_failure(rabbitmq):
    with patch(
        "alkemio_virtual_contributor_engine.rabbitmq.connect_robust",
        AsyncMock(side_effect=Exception("Connection failed")),
    ):
        with pytest.raises(Exception, match="Connection failed"):
            await rabbitmq.connect()


@pytest.mark.asyncio
async def test_consume_failure(rabbitmq):
    mock_queue = AsyncMock()
    mock_queue.consume.side_effect = Exception("consume error")
    rabbitmq.input_queue = mock_queue

    with pytest.raises(Exception, match="consume error"):
        await rabbitmq.consume(AsyncMock())


@pytest.mark.asyncio
async def test_publish_exception_handled(rabbitmq):
    mock_exchange = AsyncMock()
    mock_exchange.publish.side_effect = Exception("publish error")
    mock_channel = MagicMock()
    mock_channel.is_closed = False
    rabbitmq.exchange = mock_exchange
    rabbitmq.channel = mock_channel

    # Should not raise — publish catches exceptions
    await rabbitmq.publish({"key": "value"})


@pytest.mark.asyncio
async def test_consume_queue_failure(rabbitmq):
    mock_channel = AsyncMock()
    mock_channel.declare_queue = AsyncMock(side_effect=Exception("queue error"))
    rabbitmq.channel = mock_channel

    with pytest.raises(Exception, match="queue error"):
        await rabbitmq.consume_queue("test-queue", AsyncMock())


@pytest.mark.asyncio
async def test_publish_to_queue_failure(rabbitmq):
    mock_channel = AsyncMock()
    mock_channel.is_closed = False
    mock_channel.default_exchange = AsyncMock()
    mock_channel.default_exchange.publish.side_effect = Exception("fail")
    rabbitmq.channel = mock_channel

    # Should not raise
    await rabbitmq.publish_to_queue("test-queue", {"key": "value"})

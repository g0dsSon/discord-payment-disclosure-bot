import discord
import pytest

from unittest.mock import AsyncMock, MagicMock

from bot.logger import get_logger
from bot.types import BotConfig


@pytest.fixture
def mock_config():
    """Create mock bot configuration."""
    return BotConfig(
        token="test_token",
        prefix="!",
        log_file="test.log",
        channels=["test-channel"],
        payment_terms=["gns", "g&s", "goods and services", "goods & services"],
        required_disclosure="test disclosure"
    )


@pytest.fixture
def mock_message():
    """Create mock Discord message."""
    message = MagicMock(spec=discord.Message)
    message.author = MagicMock()
    message.author.name = "TestUser"
    message.author.send = AsyncMock()
    message.channel.name = "test-channel"
    message.content = "test message"
    message.delete = AsyncMock()
    return message


@pytest.fixture
def mock_templates():
    """Create mock message templates."""
    return {
        "dm_notification": "Hello {{ user_name }}, {{ required_disclosure }}"
    }


@pytest.fixture
def test_logger():
    """Create mock logger."""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    return logger
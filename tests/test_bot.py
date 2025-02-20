from unittest.mock import MagicMock, patch

import discord
import pytest

from bot.core import EnforcerBot


class TestEnforcerBot:
    """Test cases for EnforcerBot class."""

    @pytest.mark.asyncio
    async def test_check_message_content_with_required_terms(
        self, mock_config, mock_templates, test_logger
    ):
        """Test message content checking with payment terms."""
        test_cases = [
            ("selling keyboard g&s", True),
            ("selling keyboard G&S", True),
            ("selling keyboard goods and services", True),
            ("selling keyboard goods & services", True),
            ("selling keyboard gns", True),
        ]
        bot = EnforcerBot(test_logger, mock_config, mock_templates)
        for content, expected in test_cases:
            assert bot._check_message_content(content) == expected

    @pytest.mark.asyncio
    async def test_check_message_content_with_disclosure(
        self, mock_config, mock_templates, test_logger
    ):
        """Test message content checking with disclosure."""
        test_cases = [
            ("selling keyboard test disclosure", True),
            ("TEST DISCLOSURE keyboard", True),
            ("keyboard with Test Disclosure", True),
        ]
        bot = EnforcerBot(test_logger, mock_config, mock_templates)
        for content, expected in test_cases:
            assert bot._check_message_content(content) == expected

    @pytest.mark.asyncio
    async def test_check_message_content_invalid(
        self, mock_config, mock_templates, test_logger
    ):
        """Test message content checking with invalid content."""
        test_cases = [
            "selling keyboard",
            "f&f only",
            "paypal friends",
            "",
            None,
        ]
        bot = EnforcerBot(test_logger, mock_config, mock_templates)
        for content in test_cases:
            assert not bot._check_message_content(content)

    @pytest.mark.asyncio
    async def test_handle_violation(
        self, mock_config, mock_templates, mock_message, test_logger
    ):
        """Test successful violation handling."""
        bot = EnforcerBot(test_logger, mock_config, mock_templates)
        await bot._handle_violation(mock_message)

        mock_message.delete.assert_called_once()
        mock_message.author.send.assert_called_once()
        # Verify logger was called
        assert any(
            "Blocked message from" in str(call)
            for call in test_logger.info.call_args_list
        )

    @pytest.mark.asyncio
    async def test_handle_violation_forbidden(
        self, mock_config, mock_templates, mock_message, test_logger
    ):
        """Test violation handling when bot lacks permissions."""
        mock_message.delete.side_effect = discord.Forbidden(MagicMock(), "test")

        bot = EnforcerBot(test_logger, mock_config, mock_templates)
        await bot._handle_violation(mock_message)

        mock_message.delete.assert_called_once()
        mock_message.author.send.assert_not_called()
        # Verify warning was logged
        assert any(
            "Failed to delete message" in str(call)
            for call in test_logger.warning.call_args_list
        )

    @pytest.mark.asyncio
    async def test_on_message_handler(
        self, mock_config, mock_templates, mock_message, test_logger
    ):
        """Test message event handler."""
        bot = EnforcerBot(test_logger, mock_config, mock_templates)

        # Test bot message (should be ignored)
        mock_message.author.bot = True
        await bot.bot.on_message(mock_message)
        mock_message.delete.assert_not_called()

        # Test wrong channel
        mock_message.author.bot = False
        mock_message.channel.name = "wrong-channel"
        await bot.bot.on_message(mock_message)
        mock_message.delete.assert_not_called()

        # Test valid message
        mock_message.channel.name = "test-channel"
        mock_message.content = "selling keyboard g&s"
        await bot.bot.on_message(mock_message)
        mock_message.delete.assert_not_called()

        # Test invalid message
        mock_message.content = "selling keyboard"
        await bot.bot.on_message(mock_message)
        mock_message.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_bot_initialization(self, mock_config, mock_templates, test_logger):
        """Test bot initialization."""
        bot = EnforcerBot(test_logger, mock_config, mock_templates)
        assert bot.config == mock_config
        assert bot.templates == mock_templates
        assert bot.logger == test_logger
        assert bot.bot.command_prefix == mock_config.prefix
        assert bot.bot.intents.message_content is True

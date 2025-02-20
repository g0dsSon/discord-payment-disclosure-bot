"""Disforcer.

A Discord bot that monitors specified channels for messages, ensuring they contain
either specific terms or disclaimers.

Author: g0dSsOn
Copyright (c) 2025
License: MIT License
"""

import discord
import os
import re
import sys
import threading

from discord.ext import commands
from jinja2 import Template
from logging import Logger
from pathlib import Path
from typing import Any, Dict, Optional
from tomli import TOMLDecodeError
from yaml import YAMLError


from bot.config import load_config
from bot.logger import get_logger
from bot.server import run_server
from bot.types import BotConfig


class EnforcerBot:
    """Main bot class for content enforceeent."""

    def __init__(self, config: BotConfig, logger: Logger):
        """Initialize bot with configuration."""
        self.config = config
        self.logger = logger

        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix=config.prefix, intents=intents)
        self.setup_events()

    def setup_events(self) -> None:
        """Set up Discord event handlers."""

        @self.bot.event
        async def on_ready() -> None:
            """Handle bot ready event."""
            self.logger.info(f"Bot started and logged in as {self.bot.user}")

        @self.bot.event
        async def on_message(message: discord.Message) -> None:
            """Process incoming messages."""
            if message.author.bot:
                return

            if message.channel.name not in self.config.channels:
                return

            is_valid = self._check_message_content(message.content)

            if not is_valid:
                await self._handle_violation(message)

    def _check_message_content(self, content: str) -> bool:
        """Check if message contains required terms or disclaimer."""
        if not content:
            return False

        content_lower = content.lower()
        has_required_term = any(
            re.search(term, content_lower, re.IGNORECASE)
            for term in self.config.required_terms
        )
        has_disclaimer = re.search(
            self.config.required_disclosure, content_lower, re.IGNORECASE
        )
        return has_required_term or bool(has_disclaimer)

    async def _handle_violation(self, message: discord.Message) -> None:
        """Handle messages that required term rules."""
        try:
            self.logger.info(
                f"Blocked message from {message.author} in "
                f"#{message.channel.name}: {message.content}"
            )

            dm_content = Template(self.config.templates["dm_notification"]).render(
                user_name=message.author.name,
                required_terms="G&S/Goods & Services",
                required_disclosure=self.config.required_disclosure,
            )

            await message.delete()
            await message.author.send(dm_content)

        except discord.Forbidden:
            self.logger.warning(
                f"Failed to delete message from {message.author} in "
                f"#{message.channel.name}: {message.content}"
            )

    def run(self) -> None:
        """Start the bot."""
        self.bot.run(self.config.token)


def main() -> None:
    """Main entry point for the bot."""
    # Allow override of config path through environment variable
    config_path = os.getenv("BOT_CONFIG_PATH")
    config_path = Path(config_path) if config_path else None
    logger = get_logger()

    # Initialize and run bot as before
    try:
        conf = load_config(config_path)
    except (FileNotFoundError, TOMLDecodeError, YAMLError) as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)

    # Start web server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True, args=[conf])
    server_thread.start()

    # Start the discord bot   
    bot = EnforcerBot(conf, logger)

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

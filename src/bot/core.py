"""Discord Payment Verification Bot.

A Discord bot that monitors specified channels for messages, ensuring they contain
either secure payment terms or a specific disclaimer.

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
from typing import Dict, Any, Optional

from bot.config import initialize
from bot.server import run_server
from bot.types import BotConfig

class PaymentVerificationBot:
    """Main bot class for payment verification."""

    def __init__(self, logger: Logger, config: BotConfig, templates: Dict[str, Any]):
        """Initialize bot with configuration."""
        self.config = config
        self.logger = logger
        self.templates = templates
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(
            command_prefix=config.prefix,
            intents=intents
        )
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
        """Check if message contains required payment terms or disclaimer."""
        if not content:
            return False
            
        content_lower = content.lower()
        has_secure_payment = any(
            re.search(term, content_lower, re.IGNORECASE)
            for term in self.config.payment_terms
        )
        has_disclaimer = re.search(
            self.config.required_disclosure,
            content_lower,
            re.IGNORECASE
        )
        return has_secure_payment or bool(has_disclaimer)


    async def _handle_violation(self, message: discord.Message) -> None:
        """Handle messages that violate payment term rules."""
        try:
            self.logger.info(
                f"Blocked message from {message.author} in "
                f"#{message.channel.name}: {message.content}"
            )
            
            dm_content = Template(self.templates["dm_notification"]).render(
                user_name=message.author.name,
                secure_terms="G&S/Goods & Services",
                required_disclosure=self.config.required_disclosure
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
    
    # Start web server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Initialize and run bot as before
    conf, logger, templates = initialize(config_path)
    bot = PaymentVerificationBot(conf, logger, templates)
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

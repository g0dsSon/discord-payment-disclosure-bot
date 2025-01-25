"""Payment Verification Bot package.

This package provides functionality for monitoring Discord channels
and enforcing payment disclosure rules.
"""

from bot.config import initialize
from bot.core import PaymentVerificationBot
from bot.logger import get_logger
from bot.types import BotConfig

__version__ = "1.0.0"
__author__ = "g0dSsOn"
__license__ = "MIT"

__all__ = [
    "BotConfig",
    "PaymentVerificationBot",
    "initialize",
    "get_logger",
]

"""Enforcer Bot package.

This package provides functionality for monitoring Discord channels
and enforcing terms or disclosure rules.
"""

from bot.config import load_config
from bot.core import EnforcerBot
from bot.logger import get_logger
from bot.types import BotConfig

__version__ = "1.0.0"
__author__ = "g0dSsOn"
__license__ = "MIT"

__all__ = [
    "BotConfig",
    "EnforcerBot",
    "load_config",
    "get_logger",
]

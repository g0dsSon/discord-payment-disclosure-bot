import sys
import tomli
import yaml

from logging import Logger
from pathlib import Path
from typing import Any, Dict, Optional

from bot.logger import get_logger
from bot.types import BotConfig, ServerConfig


def load_config(config_path: Optional[Path] = None) -> BotConfig:
    """Load configuration and templates."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.toml"

    with open(config_path, "rb") as f:
        config = tomli.load(f)

    template_path = Path(__file__).parent.parent / "config" / "templates" / "messages.yaml"
    with open(template_path, "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)

    server_config = ServerConfig(
        host=config["bot"]["server"]["host"],
        port=config["bot"]["server"]["port"],
        workers=config["bot"]["server"]["workers"],
        log_level=config["bot"]["server"]["log_level"],
        reload=config["bot"]["server"]["reload"],
    )

    return (
        BotConfig(
            prefix=config["bot"]["prefix"],
            token=config["bot"]["token"],
            channels=config["bot"]["monitoring"]["channels_to_monitor"],
            required_terms=config["bot"]["monitoring"]["required_terms"],
            required_disclosures=config["bot"]["monitoring"]["required_disclosures"],
            server=server_config,
            templates=templates
        )
    )

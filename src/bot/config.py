
import sys
import tomli
import yaml

from logging import Logger
from pathlib import Path
from typing import Any, Dict, Optional

from bot.logger import get_logger
from bot.types import BotConfig, ServerConfig


def initialize(config_path: Optional[Path] = None) -> tuple[BotConfig, Dict[str, Any], Logger]:
    """Load configuration and templates."""
    try:
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "config.toml"
        
        with open(config_path, "rb") as f:
            config = tomli.load(f)
        
        template_path = Path(__file__).parent / "config" / "templates" / "messages.yaml"
        with open(template_path, "r", encoding='utf-8') as f:
            templates = yaml.safe_load(f)

        logger = get_logger(config.log_file)

        server_config = ServerConfig(
            host=config["server"]["host"],
            port=config["server"]["port"],
            workers=config["server"]["workers"],
            log_level=config["server"]["log_level"],
            reload=config["server"]["reload"]
        )

        return BotConfig(
            token=config["bot"]["token"],
            prefix=config["bot"]["prefix"],
            channels=config["monitoring"]["channels_to_monitor"],
            payment_terms=config["monitoring"]["secure_payment_terms"],
            required_disclosure=config["messages"]["required_disclosure"],
            server=server_config
        ), templates, logger
    except (FileNotFoundError, tomli.TOMLDecodeError, yaml.YAMLError) as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)


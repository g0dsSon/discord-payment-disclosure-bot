from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class ServerConfig:
    """Configuration for the web server."""
    host: str
    port: int
    workers: int
    log_level: str
    reload: bool

@dataclass
class BotConfig:
    """Configuration container for bot settings."""
    token: str
    prefix: str
    channels: list[str]
    required_terms: list[str]
    required_disclosures: list[str]
    server: ServerConfig
    templates: Dict[str, Any]
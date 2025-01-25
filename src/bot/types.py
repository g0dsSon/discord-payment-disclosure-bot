from dataclasses import dataclass

@dataclass
class BotConfig:
    """Configuration container for bot settings."""
    token: str
    prefix: str
    log_file: str
    channels: list[str]
    payment_terms: list[str]
    required_disclosure: str

@dataclass
class ServerConfig:
    """Configuration for the web server."""
    host: str
    port: int
    workers: int
    log_level: str
    reload: bool

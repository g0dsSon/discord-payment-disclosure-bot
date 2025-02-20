import logging

DEFAULT_LOG_FILE="bot.log"

def configure() -> None:
    """Configure logging with specified file."""
    logging.basicConfig(
        filename=DEFAULT_LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(leimport loggingvelname)s - %(message)s",
        encoding="utf-8",
    )


def get_logger() -> logging.Logger:
    """Initialize logging with specified file."""
    configure()
    return logging.getLogger()

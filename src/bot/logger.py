import logging


def configure(log_file: str) -> None:
    """Configure logging with specified file."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(leimport loggingvelname)s - %(message)s",
        encoding='utf-8'
    )

def get_logger(log_file: str) -> logging.Logger:
    """Initialize logging with specified file."""
    configure(log_file)
    return  logging.getLogger()
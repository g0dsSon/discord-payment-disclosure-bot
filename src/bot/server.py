import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from bot.logger import get_logger
from bot.types import BotConfig

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "healthy"}


@app.get("/callback")
async def callback(code: str):
    return RedirectResponse(url="/")


def override_logging(log_file: str) -> None:
    # Configure uvicorn loggers to use bot's logger
    for name in ["uvicorn", "uvicorn.access", "uvicorn.error", "uvicorn.asgi"]:
        uvicorn_logger = get_logger(log_file)
        uvicorn_logger.handlers = []  # Remove default handlers
        uvicorn_logger.propagate = True  # Propagate to parent logger
        uvicorn_logger.setLevel(uvicorn_logger.level)


def run_server(config: BotConfig):
    override_logging(config.log_file)

    server_config = config.server

    config = uvicorn.Config(
        app="bot.server:app",
        host=server_config.host,
        port=server_config.port,
        reload=server_config.reload,
        workers=server_config.workers,
        log_config=None,
    )
    server = uvicorn.Server(config)
    server.run()

FROM python:3.10-slim

WORKDIR /bot

COPY pyproject.toml .
COPY src/ src/

RUN pip install .

CMD ["python", "-m", "bot.core"]

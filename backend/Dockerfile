FROM python:3.11-slim
LABEL authors="bhavik"

RUN apt-get update && apt-get install -y wget curl

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

ENV PYTHONPATH=/app

COPY app/ /app/app

ENTRYPOINT ["uvicorn", "app.main:app", "--workers", "8", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
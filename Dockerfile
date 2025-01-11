FROM python:3.13-slim as base

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY uv.lock pyproject.toml .

RUN pip install uv
RUN uv sync

COPY . .


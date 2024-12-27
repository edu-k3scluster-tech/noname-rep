FROM python:3.13-slim as base

WORKDIR /app

COPY uv.lock pyproject.toml .

RUN pip install uv
RUN uv sync

COPY . .


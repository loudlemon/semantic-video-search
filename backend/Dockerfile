FROM python:3.11-slim

# Устанавливаем uv вручную
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Сначала только зависимости
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Теперь копируем ВСЁ (включая созданный README.md)
COPY . .

# Собираем проект один раз при сборке образа
# Вместо старого шага 20:
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project


# В CMD используем флаг --no-sync, чтобы uv не пытался ничего пересобирать при старте
CMD ["uv", "run", "--no-sync", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


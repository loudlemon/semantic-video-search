FROM astral-sh/uv:python3.11-slim AS builder

# Enable bytecode compilation for faster startups
ENV UV_COMPILE_BYTECODE=1
# Use the copy mode instead of symlinks for the virtualenv
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first (layer caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Final stage: just run the app using 'uv run'
# This ensures we use the synced environment
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

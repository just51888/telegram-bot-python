FROM python:3.12-slim

RUN mkdir -p /app
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip uv==0.5.29

ENV UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

RUN uv sync --no-debug --no-install-project

COPY . .

RUN uv sync --no-debug

CMD ["uv", "run", "python", "main.py"]

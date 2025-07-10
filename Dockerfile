FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -Ls https://astral.sh/uv/install.sh | bash

RUN ln -s /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

COPY . /app

RUN uv sync

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

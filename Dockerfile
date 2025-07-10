FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -Ls https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.cargo/bin:$PATH"
RUN /root/.cargo/bin/uv --version

WORKDIR /app

COPY . /app

RUN uv sync

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

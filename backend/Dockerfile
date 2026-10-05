FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . .
RUN chmod +x /app/entrypoint.dev.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.dev.sh"]

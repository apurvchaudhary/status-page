FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get update && apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

RUN apt-get purge -y build-essential && apt-get autoremove -y && apt-get clean

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=production

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /uploads

COPY ./config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY wait-for-postgres.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
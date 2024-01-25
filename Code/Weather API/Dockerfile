FROM python:3.8.13-slim-buster

EXPOSE 8000
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

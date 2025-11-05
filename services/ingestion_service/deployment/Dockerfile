FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion_service ./ingestion_service
ENV PYTHONPATH=/app/ingestion_service

EXPOSE 8001
CMD ["python", "-m", "ingestion_service.components.composites.main"]

FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY embedding_service/main.py ./embedding_service
ENV PYTHONPATH=/app/embedding_service

EXPOSE 8000
CMD ["python", "-m", "embedding_service.main"]

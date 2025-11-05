FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./captioning_service
ENV PYTHONPATH=/app/captioning_service

EXPOSE 8002
CMD ["python", "-m", "captioning_service.main"]

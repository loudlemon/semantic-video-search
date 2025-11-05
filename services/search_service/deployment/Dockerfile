FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./indexing_service
ENV PYTHONPATH=/app/search_service

EXPOSE 8080
CMD ["python", "-m", "search_service.components.composites.main"]

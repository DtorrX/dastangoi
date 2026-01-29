FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir fastapi uvicorn boto3 requests

COPY src /app/src

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8002"]

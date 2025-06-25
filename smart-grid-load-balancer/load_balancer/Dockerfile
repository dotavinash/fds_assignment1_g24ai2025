FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask prometheus_client requests

CMD ["python3", "main.py"]

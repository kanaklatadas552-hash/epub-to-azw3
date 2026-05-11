FROM python:3.11-slim

RUN apt-get update && apt-get install -y calibre && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install fastapi uvicorn python-multipart

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]

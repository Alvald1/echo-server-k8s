FROM python:3.11-slim

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD python main.py

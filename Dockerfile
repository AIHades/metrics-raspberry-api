FROM python:3.12.3-slim

MAINTAINER Hades
LABEL name="webapp" \
      version="1.0"

WORKDIR /opt/app

COPY backend/requirements.txt ./backend/requirements.txt 

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

COPY backend ./backend
COPY frontend ./frontend 

ENTRYPOINT ["python3", "backend/main.py"]
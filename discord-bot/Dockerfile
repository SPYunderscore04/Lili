FROM python:3.12
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src

ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
CMD python src/main.py

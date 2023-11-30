FROM python:3.10-alpine

COPY . /app

WORKDIR /app
RUN apk add --no-cache \
    build-base \
    gdal-dev

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "main.py"]

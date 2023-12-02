FROM python:3.10-alpine
RUN apk update
RUN apk add --no-cache gdal-dev build-base
COPY . /app

WORKDIR /app

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install numpy
RUN pip install gdal==$(gdal-config --version) 

CMD ["python", "main.py"]
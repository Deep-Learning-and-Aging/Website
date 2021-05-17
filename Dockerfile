FROM python:latest

RUN mkdir /website
WORKDIR /website

COPY setup.py .
COPY /dash_website .
COPY /data .
COPY app.yaml .

RUN pip install -e .

CMD exec gunicorn --bind 0.0.0.0:8080 'dash_website.index:get_server()'
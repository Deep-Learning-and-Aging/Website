FROM python:latest

RUN mkdir /website
WORKDIR /website

COPY setup.py .
COPY /dash_website .

RUN pip install -e .

# COPY /data .

CMD exec gunicorn --bind 0.0.0.0:8080 'dash_website.index:get_server()'
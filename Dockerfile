FROM python:latest

RUN mkdir /website
WORKDIR /website

COPY . .

RUN pip install -e .

CMD exec gunicorn --bind 0.0.0.0:8080 'dash_website.index:get_server()'
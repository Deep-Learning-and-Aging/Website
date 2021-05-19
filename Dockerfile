FROM python:latest

RUN mkdir /website
WORKDIR /website

COPY . .

RUN pip install -e .

CMD exec gunicorn --bind 0.0.0.0:8080 'dash_website.index:get_server()'

# docker build -t gcr.io/age-prediction-306519/website .
# docker run -p 8080:8080 gcr.io/age-prediction-306519/website
# syntax=docker/dockerfile:1

FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -ms /bin/bash python
WORKDIR /home/python/code

COPY requirements.txt /home/python/code/
RUN apt-get update && apt-get install -y g++ gcc musl-dev libpq-dev && \
  pip3 install --upgrade pip setuptools && \
  pip3 install -r requirements.txt --no-cache-dir && \
  rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY . .

ENV DJANGO_SUPERUSER_USERNAME=signoz
ENV DJANGO_SUPERUSER_PASSWORD=password
ENV DJANGO_SUPERUSER_EMAIL=hello@signoz.io
# ENV DJANGO_SETTINGS_MODULE=mysite.settings

ENV OTEL_LOG_LEVEL=debug
ENV OTEL_TRACES_EXPORTER=console,otlp

RUN python manage.py migrate && \
  python manage.py collectstatic --noinput && \
  python manage.py createsuperuser --no-input && \
  pip install setuptools && \
  opentelemetry-bootstrap --action=install

CMD [ "opentelemetry-instrument", "gunicorn", "mysite.wsgi", "-c", "gunicorn.config.py", "--workers", "2", "--threads", "2", "--bind", "0.0.0.0:8000" ]

EXPOSE 8000

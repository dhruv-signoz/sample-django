# Preparing Django app

1. `python3 manage.py migrate`
2. `python3 manage.py collectstatic`
3. `python3 manage.py createsuperuser`

# Running with SigNoz

- Create a virtual environment and activate it

```
python -m venv .venv
source .venv/bin/activate
```

- Install requirements

```
pip install -r requirements.txt
```

- Install instrumentation packages

```
opentelemetry-bootstrap --action=install
```

## Latest Python local testing

Use Python 3.13.

## To run with gunicorn you need to add post_fork hook

1. Add a file `gunicorn.config.py` as given in this repo
2. Specify that config file when running gunicorn with `opentelemetry-instrument`

```
DJANGO_SETTINGS_MODULE=<DJANGO_APP>.settings \
OTEL_TRACES_EXPORTER=console,otlp \
OTEL_METRICS_EXPORTER=none \
OTEL_RESOURCE_ATTRIBUTES=service.name=<serviceName> \
OTEL_EXPORTER_OTLP_ENDPOINT=https://<YOUR-SIGNOZ-CLOUD-INGEST-HOST>:443 \
OTEL_EXPORTER_OTLP_HEADERS=signoz-ingestion-key=<YOUR_INGESTION_KEY> \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
opentelemetry-instrument gunicorn <DJANGO_APP>.wsgi -c gunicorn.config.py --workers 2 --threads 2
```
*specifying **DJANGO_SETTINGS_MODULE** is necessary for opentelemetry instrumentation to work*

**For this example, sample command would look like**

```
DJANGO_SETTINGS_MODULE=mysite.settings \
OTEL_TRACES_EXPORTER=console,otlp \
OTEL_METRICS_EXPORTER=none \
OTEL_RESOURCE_ATTRIBUTES=service.name=sample-django-app \
OTEL_EXPORTER_OTLP_ENDPOINT=https://ingest.<region>.signoz.cloud:443 \
OTEL_EXPORTER_OTLP_HEADERS=signoz-ingestion-key=<YOUR_INGESTION_KEY> \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
DEVELOPMENT_MODE=True \
opentelemetry-instrument gunicorn mysite.wsgi -c gunicorn.config.py --workers 2 --threads 2
```

Note: set `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` if you are using OTLP HTTP exporter.

# If want to run docker image of django app directly 
```
docker run --env \
    --env OTEL_RESOURCE_ATTRIBUTES=service.name=sample-django-app \
    --env OTEL_TRACES_EXPORTER=console,otlp \
    --env OTEL_METRICS_EXPORTER=none \
    --env OTEL_EXPORTER_OTLP_ENDPOINT=https://ingest.<region>.signoz.cloud:443 \
    --env OTEL_EXPORTER_OTLP_HEADERS=signoz-ingestion-key=<YOUR_INGESTION_KEY> \
    --env OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
    --env DJANGO_SETTINGS_MODULE=mysite.settings \
    --env DEVELOPMENT_MODE=True \
    -p 8000:8000 \
    -t signoz/sample-django:latest
```

# Browsing the app and checking at SigNoz

1. Visit `http://localhost:8000/admin` and create a question for poll
2. Then visit the list of polls at `http://localhost:8000/polls/` and explore the polls
3. The data should be visible now in SigNoz at `http://<IP of SigNoz>:3000`




import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# from otel_config import init_otel


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


    print("initializing opentelemtry SDK in the gunicorn.config.py")
    init_otel()


    tracer = trace.get_tracer("app")

    with tracer.start_as_current_span("manual-from-gunicorn") as span:
        print("span!!! inside gunciorn fork", span)
        span.set_attribute("key", "value")


import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor



def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    resource = Resource.create(attributes={
        "service.name": "api-service"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint="https://ingest.in.signoz.cloud:443",
            headers={
                "signoz-ingestion-key": "<your-ingestion-key-here>"
            }
        )
    )

    # export to both console and otlp for testing
    trace.get_tracer_provider().add_span_processor(span_processor)
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    print("initializing opentelemtry SDK in the gunicorn.config.py")

    # create span to see if the configuration works or still emits unauthenticated transient error!
    tracer = trace.get_tracer("app")

    with tracer.start_as_current_span("manual-from-gunicorn") as span:
        print("span!!! inside gunciorn fork", span)
        span.set_attribute("key", "value")


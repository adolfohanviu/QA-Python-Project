import json
import logging
import os
import socket
import uuid
from contextlib import contextmanager
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator, cast
from urllib.parse import urlparse

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.util.types import AttributeValue

_trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="")
_state = {"initialized": False, "file_handler_attached": False}


def observability_enabled() -> bool:
    return os.getenv("OBSERVABILITY_ENABLED", "false").lower() == "true"


def current_trace_id() -> str:
    return _trace_id_ctx.get()


def set_trace_id(trace_id: str) -> Token:
    return _trace_id_ctx.set(trace_id)


def reset_trace_id(token: Token) -> None:
    _trace_id_ctx.reset(token)


def new_trace_id() -> str:
    return uuid.uuid4().hex


def _json_logger() -> logging.Logger:
    return logging.getLogger("qa.observability")


def _endpoint_reachable(endpoint: str, timeout_seconds: float = 1.0) -> bool:
    parsed = urlparse(endpoint)
    host = parsed.hostname
    if not host:
        return False

    if parsed.port is not None:
        port = parsed.port
    elif parsed.scheme == "https":
        port = 443
    else:
        port = 80

    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def configure_observability_file_logging(log_file: str = "logs/qa-tests.log") -> None:
    if _state["file_handler_attached"]:
        return

    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger = _json_logger()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)

    _state["file_handler_attached"] = True


def init_observability(service_name: str = "qa-portfolio-tests") -> None:
    if _state["initialized"]:
        return

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    if not endpoint:
        base = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
        endpoint = f"{base.rstrip('/')}/v1/traces"

    if not _endpoint_reachable(endpoint):
        _json_logger().warning("OTLP endpoint is unreachable, skipping trace exporter init: %s", endpoint)
        return

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))

    trace.set_tracer_provider(provider)
    _state["initialized"] = True


def shutdown_observability() -> None:
    provider = trace.get_tracer_provider()
    shutdown_method = getattr(provider, "shutdown", None)
    if shutdown_method is not None:
        cast(Callable[[], None], shutdown_method)()


def emit_event(event: str, **fields: Any) -> None:
    payload: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "trace_id": current_trace_id(),
    }
    payload.update(fields)
    _json_logger().info(json.dumps(payload, ensure_ascii=True))


def _to_attribute_value(value: Any) -> AttributeValue:
    """Convert arbitrary values to OpenTelemetry-supported attribute values."""
    if isinstance(value, (str, bool, int, float)):
        return value

    if isinstance(value, (list, tuple)):
        if all(isinstance(item, str) for item in value):
            return list(value)
        if all(isinstance(item, bool) for item in value):
            return list(value)
        if all(isinstance(item, int) and not isinstance(item, bool) for item in value):
            return list(value)
        if all(isinstance(item, float) for item in value):
            return list(value)

    # Fallback keeps attributes serializable and avoids runtime/type errors.
    return str(value)


@contextmanager
def traced_span(name: str, **attributes: Any) -> Iterator[object]:
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            span.set_attribute(key, _to_attribute_value(value))

        span_context = span.get_span_context()
        if span_context and span_context.trace_id:
            trace_id = f"{span_context.trace_id:032x}"
            token = set_trace_id(trace_id)
            try:
                yield span
            finally:
                reset_trace_id(token)
        else:
            yield span

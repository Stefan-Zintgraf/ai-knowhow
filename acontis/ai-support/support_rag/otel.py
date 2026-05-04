"""Optional OpenTelemetry (NFR-4) — gRPC OTLP to collector."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from support_rag.config import AppConfig

logger = logging.getLogger(__name__)


def setup_telemetry(config: AppConfig) -> None:
    ep = (config.observability.otel_endpoint or "").strip()
    if not ep:
        return
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError as e:
        logger.warning("OTel SDK not available: %s", e)
        return
    res = Resource.create(
        {
            "service.name": config.observability.service_name,
        }
    )
    prov = TracerProvider(resource=res)
    prov.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=ep, insecure=True))
    )
    trace.set_tracer_provider(prov)
    logger.info("OpenTelemetry export enabled -> %s", ep)

# Python 3.12 — ML stack (sentence-transformers, etc.) is not available on 3.14 in many images.
FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir -U pip hatchling
COPY pyproject.toml README.md config.example.yaml /app/
COPY support_rag /app/support_rag
RUN pip install --no-cache-dir -e /app
ENV RAG_CONFIG=/app/config.yaml
EXPOSE 8080
CMD ["uvicorn", "support_rag.app:app", "--host", "0.0.0.0", "--port", "8080"]
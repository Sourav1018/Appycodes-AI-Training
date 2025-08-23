# app/db/qdrant_conn.py
from qdrant_client import QdrantClient

from app.config.app_config import settings

_qdrant_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=settings.QDRANT_CLUSTER_URL, api_key=settings.QDRANT_API_KEY
        )
    return _qdrant_client


def close_qdrant_client():
    global _qdrant_client
    if _qdrant_client is not None:
        _qdrant_client.close()
        _qdrant_client = None

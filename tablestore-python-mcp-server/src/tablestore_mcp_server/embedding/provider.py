import logging

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from tablestore_mcp_server.embedding.type import EmbeddingProviderType
from tablestore_mcp_server.settings import EmbeddingProviderSettings

logger = logging.getLogger(__name__)


def create_embedding(settings: EmbeddingProviderSettings) -> BaseEmbedding:
    logger.info(f"Using embedding provider {settings.provider_type} with model {settings.model_name}")
    if settings.model_name is None or len(settings.model_name) == 0:
        raise ValueError("`model_name` is empty")
    if settings.provider_type == EmbeddingProviderType.HUGGING_FACE:
        embed_model = HuggingFaceEmbedding(model_name=settings.model_name)
        return embed_model
    else:
        raise ValueError(f"unsupported embedding type: {settings.provider_type}")

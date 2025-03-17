import os

import numpy as np
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import tablestore_mcp_server.embedding.provider as embedding_provider
import tablestore_mcp_server.settings as settings


class TestEmbeddingProvider:
    def test_initialization(self):
        provider = embedding_provider.create_embedding(settings.EmbeddingProviderSettings())
        assert provider.model_name == "BAAI/bge-base-zh-v1.5"
        assert isinstance(provider, BaseEmbedding)
        assert isinstance(provider, HuggingFaceEmbedding)

    def test_other_embedding(self):
        test_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        os.environ["EMBEDDING_MODEL_NAME"] = test_model_name
        try:
            provider = embedding_provider.create_embedding(settings.EmbeddingProviderSettings())
            assert provider.model_name == test_model_name
            assert isinstance(provider, BaseEmbedding)
            assert isinstance(provider, HuggingFaceEmbedding)

            document = "这是一个测试文档"
            embedding = provider.get_text_embedding(document)
            assert len(embedding) == 384
        finally:
            os.environ.pop("EMBEDDING_MODEL_NAME")

    def test_embed_documents(self):
        provider = embedding_provider.create_embedding(settings.EmbeddingProviderSettings())
        assert provider.model_name == "BAAI/bge-base-zh-v1.5"
        document1 = "这是一个测试文档"
        document2 = "这是另一个测试文档"

        embedding1 = provider.get_text_embedding(document1)
        embedding2 = provider.get_text_embedding(document2)

        assert len(embedding1) == 768
        assert len(embedding2) == 768
        assert not np.array_equal(np.array(embedding1), np.array(embedding2))

    def test_embed_query(self):
        provider = embedding_provider.create_embedding(settings.EmbeddingProviderSettings())
        assert provider.model_name == "BAAI/bge-base-zh-v1.5"
        query = "这是一个测试查询语句"

        embedding1 = provider.get_query_embedding(query)
        assert len(embedding1) > 0

        embedding2 = provider.get_query_embedding(query)
        assert len(embedding1) == len(embedding2)

        np.testing.assert_array_almost_equal(np.array(embedding1), np.array(embedding2))

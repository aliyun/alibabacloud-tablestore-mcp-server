import pytest
from llama_index.core.base.embeddings.base import BaseEmbedding

import tablestore_mcp_server.embedding.provider as embedding_provider
import tablestore_mcp_server.settings as settings
from tablestore_mcp_server.tablestore_connector import TablestoreConnector, Entry


@pytest.fixture
def embedding() -> BaseEmbedding:
    provider = embedding_provider.create_embedding(settings.EmbeddingProviderSettings())
    return provider


# noinspection PyProtectedMember
@pytest.fixture
def tablestore_connector(embedding):
    tablestore_settings = settings.TablestoreSettings()
    if (
        tablestore_settings.end_point is None
        or tablestore_settings.instance_name is None
        or tablestore_settings.access_key_id is None
        or tablestore_settings.access_key_secret is None
    ):
        pytest.skip("end_point is None or instance_name is None or access_key_id is None or access_key_secret is None")

    # 1. create tablestore vector store
    connector = TablestoreConnector(
        embedding=embedding,
        instance_name=tablestore_settings.instance_name,
        end_point=tablestore_settings.end_point,
        access_key_id=tablestore_settings.access_key_id,
        access_key_secret=tablestore_settings.access_key_secret,
        table_name=tablestore_settings.table_name,
        index_name=tablestore_settings.index_name,
        vector_dimension=tablestore_settings.vector_dimension,
        text_field=tablestore_settings.text_field,
        vector_field=tablestore_settings.vector_field,
    )
    connector._store.create_table_if_not_exist()
    connector._store.create_search_index_if_not_exist()
    return connector


def test_store_and_search(tablestore_connector):
    """Test storing an entry and then searching for it."""
    # Store a test entry
    test_entry = Entry(
        content="我是一个小学生，我擅长王者荣耀",
        metadata={"source": "test", "level": "high"},
    )
    tablestore_connector.store(test_entry)

    # Search for the entry
    results = tablestore_connector.search("我是一个小学生，我擅长王者荣耀")

    # Verify results
    assert len(results) >= 1
    assert results[0].content == test_entry.content
    assert results[0].metadata == test_entry.metadata

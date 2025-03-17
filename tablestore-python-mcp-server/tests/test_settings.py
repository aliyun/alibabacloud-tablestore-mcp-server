import os
from unittest.mock import patch

from tablestore_mcp_server.embedding.type import EmbeddingProviderType
from tablestore_mcp_server.settings import ToolSettings, DEFAULT_TOOL_STORE_DESCRIPTION, DEFAULT_TOOL_SEARCH_DESCRIPTION, EmbeddingProviderSettings, TablestoreSettings


class TestTablestoreSettings:
    @patch.dict(
        os.environ,
        {
            "TABLESTORE_INSTANCE_NAME": "abc",
            "TABLESTORE_ENDPOINT": "http://localhost:80",
            "TABLESTORE_ACCESS_KEY_ID": "xx",
            "TABLESTORE_ACCESS_KEY_SECRET": "xxx",
        },
    )
    def test_minimal_setting(self):
        settings = TablestoreSettings()
        assert settings.instance_name is not None
        assert settings.end_point is not None
        assert settings.access_key_id is not None
        assert settings.access_key_secret is not None


class TestEmbeddingProviderSettings:
    def test_default_values(self):
        settings = EmbeddingProviderSettings()
        assert settings.provider_type == EmbeddingProviderType.HUGGING_FACE
        assert settings.model_name == "BAAI/bge-base-zh-v1.5"

    @patch.dict(
        os.environ,
        {"EMBEDDING_MODEL_NAME": "custom_model"},
    )
    def test_custom_values(self):
        settings = EmbeddingProviderSettings()
        assert settings.provider_type == EmbeddingProviderType.HUGGING_FACE
        assert settings.model_name == "custom_model"


class TestToolSettings:
    def test_default_values(self):
        settings = ToolSettings()
        assert settings.tool_store_description == DEFAULT_TOOL_STORE_DESCRIPTION
        assert settings.tool_search_description == DEFAULT_TOOL_SEARCH_DESCRIPTION

    @patch.dict(
        os.environ,
        {"TOOL_STORE_DESCRIPTION": "Custom store description"},
    )
    def test_custom_store_description(self):
        settings = ToolSettings()
        assert settings.tool_store_description == "Custom store description"
        assert settings.tool_search_description == DEFAULT_TOOL_SEARCH_DESCRIPTION

    @patch.dict(
        os.environ,
        {"TOOL_SEARCH_DESCRIPTION": "Custom search description"},
    )
    def test_custom_search_description(self):
        settings = ToolSettings()
        assert settings.tool_store_description == DEFAULT_TOOL_STORE_DESCRIPTION
        assert settings.tool_search_description == "Custom search description"

    @patch.dict(
        os.environ,
        {
            "TOOL_STORE_DESCRIPTION": "Custom store description",
            "TOOL_SEARCH_DESCRIPTION": "Custom search description",
        },
    )
    def test_all_custom_values(self):
        settings = ToolSettings()
        assert settings.tool_store_description == "Custom store description"
        assert settings.tool_search_description == "Custom search description"

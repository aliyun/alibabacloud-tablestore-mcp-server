from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

from tablestore_mcp_server.embedding.type import EmbeddingProviderType

DEFAULT_TOOL_STORE_DESCRIPTION = """
Store document into Tablestore(表格存储) for later retrieval. 

The input parameter: 
1. The 'information' parameter should contain a natural language document content. 
2. The 'metadata' parameter is a Python dictionary with strings as keys, which can store some meta data related to this document.
"""
DEFAULT_TOOL_SEARCH_DESCRIPTION = """
Search for similar documents on natural language descriptions from Tablestore(表格存储).

The input parameter: 
1. The 'query' parameter should describe what you're looking for, and the tool will return the most relevant documents.
2. The 'size' parameter: the number of similar documents to be returned.
"""


class ServerSettings(BaseSettings):
    """
    Configuration for server.
    """

    host: str = Field(default="0.0.0.0", validation_alias="SERVER_HOST")
    port: int = Field(default=8001, validation_alias="SERVER_PORT")


class ToolSettings(BaseSettings):
    """
    Configuration for tool.
    """

    tool_store_description: str = Field(
        default=DEFAULT_TOOL_STORE_DESCRIPTION,
        validation_alias="TOOL_STORE_DESCRIPTION",
    )
    tool_search_description: str = Field(
        default=DEFAULT_TOOL_SEARCH_DESCRIPTION,
        validation_alias="TOOL_SEARCH_DESCRIPTION",
    )


class EmbeddingProviderSettings(BaseSettings):
    """
    Configuration for the embedding provider.
    """

    provider_type: EmbeddingProviderType = Field(
        default=EmbeddingProviderType.HUGGING_FACE,
        validation_alias="EMBEDDING_PROVIDER_TYPE",
    )
    model_name: str = Field(
        default="BAAI/bge-base-zh-v1.5",
        alias="EMBEDDING_MODEL_NAME",
    )


class TablestoreSettings(BaseSettings):
    """
    Configuration for Tablestore.
    """

    instance_name: Optional[str] = Field(validation_alias="TABLESTORE_INSTANCE_NAME")
    end_point: Optional[str] = Field(validation_alias="TABLESTORE_ENDPOINT")
    access_key_id: Optional[str] = Field(validation_alias="TABLESTORE_ACCESS_KEY_ID")
    access_key_secret: Optional[str] = Field(validation_alias="TABLESTORE_ACCESS_KEY_SECRET")
    table_name: str = Field(default="ts_mcp_server_py_v1", validation_alias="TABLESTORE_TABLE_NAME")
    index_name: str = Field(default="ts_mcp_server_py_index_v1", validation_alias="TABLESTORE_INDEX_NAME")
    vector_dimension: int = Field(default=768, validation_alias="TABLESTORE_VECTOR_DIMENSION")
    text_field: str = Field(default="_content", validation_alias="TABLESTORE_TEXT_FIELD")
    vector_field: str = Field(default="_embedding", validation_alias="TABLESTORE_VECTOR_FIELD")

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

from tablestore_mcp_server.embedding.type import EmbeddingProviderType

DEFAULT_TOOL_STORE_DESCRIPTION = """
将文档存储到Tablestore（表格存储）以供后续检索。

输入参数：
1. 'information' 参数应包含自然语言的文档内容。
2. 'metadata' 参数是一个Python字典，键为字符串，可以存储与该文档相关的元数据。
"""
DEFAULT_TOOL_SEARCH_DESCRIPTION = """
从Tablestore(表格存储)中使用自然语言形式的文本来搜索相似性文档。

输入参数： 
1. 'query' 参数应该描述你正在寻找的内容，该工具将返回最相关的文档。
2. 'size' 参数：要返回的相似文档的数量。
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

    dash_scope_api_key: str = Field(
        default="",
        validation_alias="DASHSCOPE_API_KEY",
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

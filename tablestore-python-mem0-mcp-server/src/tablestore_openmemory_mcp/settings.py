from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field

DEFAULT_TOOL_ADD_MEMORIES_DESCRIPTION = (
    "Add a new memory. This method is called everytime the user informs anything about themselves, "
    "their preferences, or anything that has any relevant information which can be useful in the future conversation. "
    "This can also be called when the user asks you to remember something."
)
DEFAULT_TOOL_SEARCH_MEMORIES_DESCRIPTION = "Search through stored memories. This method is called EVERYTIME the user asks anything."
DEFAULT_TOOL_LIST_MEMORIES_DESCRIPTION = "List all memories in the user's memory"
DEFAULT_TOOL_DELETE_ALL_MEMORIES_DESCRIPTION = "Delete all memories in the user's memory"


class ToolSettings(BaseSettings):
    """
    Configuration for tool description.
    """

    tool_add_memories_description: str = Field(
        default=DEFAULT_TOOL_ADD_MEMORIES_DESCRIPTION,
        validation_alias="TOOL_ADD_MEMORIES_DESCRIPTION",
    )
    tool_search_memories_description: str = Field(
        default=DEFAULT_TOOL_SEARCH_MEMORIES_DESCRIPTION,
        validation_alias="TOOL_SEARCH_MEMORIES_DESCRIPTION",
    )
    tool_list_memories_description: str = Field(
        default=DEFAULT_TOOL_LIST_MEMORIES_DESCRIPTION,
        validation_alias="TOOL_LIST_MEMORIES_DESCRIPTION",
    )
    tool_delete_all_memories_description: str = Field(
        default=DEFAULT_TOOL_DELETE_ALL_MEMORIES_DESCRIPTION,
        validation_alias="TOOL_DELETE_ALL_MEMORIES_DESCRIPTION",
    )


class StdioNameSettings(BaseSettings):
    user_id: str = Field(default="stdio_default_user", validation_alias="MCP_STDIO_USER_ID")
    client_name: str = Field(default="stdio_default_client", validation_alias="MCP_STDIO_CLIENT_NAME")


class ServerSettings(BaseSettings):
    """
    Configuration for server.
    """

    host: str = Field(default="0.0.0.0", validation_alias="SERVER_HOST")
    port: int = Field(default=8765, validation_alias="SERVER_PORT")


class LLMSettings(BaseSettings):
    """
    Configuration for llm.
    """

    model: str = Field(default="qwen-plus", validation_alias="LLM_MODEL")
    api_key: str = Field(validation_alias="OPENAI_API_KEY")
    openai_base_url: str = Field(validation_alias="OPENAI_BASE_URL")


class EmbedderSettings(BaseSettings):
    """
    Configuration for embedder.
    """

    model: str = Field(default="text-embedding-v4", validation_alias="EMBEDDER_MODEL")
    api_key: str = Field(validation_alias="OPENAI_API_KEY")
    openai_base_url: str = Field(validation_alias="OPENAI_BASE_URL")


class VectorStoreSettings(BaseSettings):
    """
    Configuration for vector store.
    """

    vector_dimension: int = Field(default=1536, validation_alias="TABLESTORE_VECTOR_DIMENSION")
    endpoint: str = Field(validation_alias="TABLESTORE_ENDPOINT")
    instance_name: str = Field(validation_alias="TABLESTORE_INSTANCE_NAME")
    access_key_id: str = Field(validation_alias="TABLESTORE_ACCESS_KEY_ID")
    access_key_secret: str = Field(validation_alias="TABLESTORE_ACCESS_KEY_SECRET")
    sts_token: Optional[str] = Field(default=None, validation_alias="TABLESTORE_STS_TOKEN")


def get_memory_config():
    llm_settings = LLMSettings()
    embedder_settings = EmbedderSettings()
    vector_store_settings = VectorStoreSettings()

    return {
        "llm": {
            "provider": "openai",
            "config": {
                "model": llm_settings.model,
                "api_key": llm_settings.api_key,
                "openai_base_url": llm_settings.openai_base_url,
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": embedder_settings.model,
                "api_key": embedder_settings.api_key,
                "openai_base_url": embedder_settings.openai_base_url,
            },
        },
        "vector_store": {
            "provider": "aliyun_tablestore",
            "config": {
                "vector_dimension": vector_store_settings.vector_dimension,
                "endpoint": vector_store_settings.endpoint,
                "instance_name": vector_store_settings.instance_name,
                "access_key_id": vector_store_settings.access_key_id,
                "access_key_secret": vector_store_settings.access_key_secret,
                "sts_token": vector_store_settings.sts_token,
            },
        },
    }

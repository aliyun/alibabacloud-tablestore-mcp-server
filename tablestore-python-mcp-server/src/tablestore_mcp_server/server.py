import json
import logging
from typing import List, Optional

from mcp.server.fastmcp import Context, FastMCP

from tablestore_mcp_server.settings import ToolSettings, EmbeddingProviderSettings, TablestoreSettings, ServerSettings
from tablestore_mcp_server.tablestore_connector import TablestoreConnector, Metadata, Entry

logger = logging.getLogger(__name__)

tool_settings = ToolSettings()
server_settings = ServerSettings()
embedding_settings = EmbeddingProviderSettings()
tablestore_settings = TablestoreSettings()
# 初始化 tablestore Connector
tablestore_connector = TablestoreConnector.from_settings(embedding_settings, tablestore_settings)

logger.info(f"mcp host:{server_settings.host}, port:{server_settings.port}")
mcp = FastMCP(
    name="tablestore-mcp-server",
    host=server_settings.host,
    port=server_settings.port,
)


@mcp.tool(name="tablestore-store", description=tool_settings.tool_store_description)
async def store(
    ctx: Context,
    information: str,
    metadata: Optional[Metadata] = None,
) -> str:
    entry = Entry(content=information, metadata=metadata)
    tablestore_connector.store(entry)
    return f"Remembered: {information}"


class MCPTool:
    pass


@mcp.tool(name="tablestore-search", description=tool_settings.tool_search_description)
async def search(ctx: Context, query: str, size: int = 20) -> List[str]:
    entries = tablestore_connector.search(query, size)
    if not entries and len(entries) > 0:
        return [f"No information searched for the query '{query}'"]
    content = [f"Results for the query '{query}':"]
    for entry in entries:
        # 生成一个xml格式的结果，让LLM模型更容易解析
        entry_metadata = json.dumps(entry.metadata) if entry.metadata else ""
        content.append(f"<entry><content>{entry.content}</content><metadata>{entry_metadata}</metadata></entry>")
    return content

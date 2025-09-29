import logging
import json
from typing import Dict

from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

from fastapi import FastAPI, Request
from fastapi.routing import APIRouter
import contextvars
from mem0 import Memory

from tablestore_openmemory_mcp.settings import ToolSettings, StdioNameSettings

from tablestore_openmemory_mcp.settings import get_memory_config

# Initialize MCP
mcp = FastMCP("mem0-mcp-server")

tool_settings = ToolSettings()
stdio_name_settings = StdioNameSettings()

config = get_memory_config()
memory_client = Memory.from_config(config_dict=config)

# Context variables for user_id and client_name
user_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("user_id")
client_name_var: contextvars.ContextVar[str] = contextvars.ContextVar("client_name")

client_name_key: str = "mcp_client"

# Create a router for MCP endpoints
mcp_router = APIRouter(prefix="/mcp")

# Initialize SSE transport
sse = SseServerTransport("/mcp/messages/")


def parse_memories(memories):
    # fiting for dict or list, for future updating
    if isinstance(memories, Dict) and "results" in memories:
        return memories["results"]
    return memories


@mcp.tool(description=tool_settings.tool_add_memories_description)
async def add_memories(text: str) -> str:
    uid = user_id_var.get(None)
    client_name = client_name_var.get(None)

    if not uid:
        return "Error: user_id not provided"
    if not client_name:
        return "Error: client_name not provided"

    try:
        response = memory_client.add(
            text,
            user_id=uid,
            metadata={
                "source_app": "openmemory",
                client_name_key: client_name,
            },
        )

        return json.dumps(response, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.exception(f"Error adding to memory: {e}")
        return f"Error adding to memory: {e}"


@mcp.tool(description=tool_settings.tool_search_memories_description)
async def search_memories(query: str) -> str:
    uid = user_id_var.get(None)
    client_name = client_name_var.get(None)
    if not uid:
        return "Error: user_id not provided"
    if not client_name:
        return "Error: client_name not provided"

    try:
        memories = memory_client.search(query=query, user_id=uid, limit=10, filters={client_name_key: client_name})
        memories = [memory for memory in parse_memories(memories)]

        return json.dumps(memories, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.exception(e)
        return f"Error searching memory: {e}"


@mcp.tool(description=tool_settings.tool_list_memories_description)
async def list_memories() -> str:
    uid = user_id_var.get(None)
    client_name = client_name_var.get(None)
    if not uid:
        return "Error: user_id not provided"
    if not client_name:
        return "Error: client_name not provided"

    try:
        memories = memory_client.get_all(user_id=uid, filters={client_name_key: client_name})
        memories = [memory for memory in parse_memories(memories)]
        return json.dumps(memories, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.exception(f"Error getting memories: {e}")
        return f"Error getting memories: {e}"


@mcp.tool(description=tool_settings.tool_delete_all_memories_description)
async def delete_all_memories() -> str:
    uid = user_id_var.get(None)
    client_name = client_name_var.get(None)
    if not uid:
        return "Error: user_id not provided"
    if not client_name:
        return "Error: client_name not provided"

    try:
        memories = memory_client.get_all(user_id=uid, filters={client_name_key: client_name})
        parsed_memories = parse_memories(memories)
        for memory in parsed_memories:
            memory_client.delete(memory["id"])

        return f"Successfully deleted {len(parsed_memories)} memories"
    except Exception as e:
        logging.exception(f"Error deleting memories: {e}")
        return f"Error deleting memories: {e}"


@mcp_router.get("/{client_name}/sse/{user_id}/")
@mcp_router.get("/{client_name}/sse/{user_id}")
async def handle_sse(request: Request):
    """Handle SSE connections for a specific user and client"""
    # Extract user_id and client_name from path parameters
    uid = request.path_params.get("user_id")
    user_token = user_id_var.set(uid or "")
    client_name = request.path_params.get("client_name")
    client_token = client_name_var.set(client_name or "")

    try:
        # Handle SSE connection
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                mcp._mcp_server.create_initialization_options(),
            )
    finally:
        # Clean up context variables
        user_id_var.reset(user_token)
        client_name_var.reset(client_token)


# remove tool in tool black list
if tool_settings.tool_black_list:
    for tool in tool_settings.tool_black_list:
        mcp.remove_tool(tool)


@mcp_router.post("/messages/")
async def handle_get_message(request: Request):
    return await handle_post_message(request)


async def handle_post_message(request: Request):
    """Handle POST messages for SSE"""
    try:
        body = await request.body()

        # Create a simple receive function that returns the body
        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        # Create a simple send function that does nothing
        async def send(message):
            return {}

        # Call handle_post_message with the correct arguments
        await sse.handle_post_message(request.scope, receive, send)

        # Return a success response
        return {"status": "ok"}
    finally:
        pass


def setup_mcp_server(app: FastAPI):
    """Setup MCP server with the FastAPI application"""

    # Include MCP router in the FastAPI app
    app.include_router(mcp_router)


def run_stdio():
    user_token = user_id_var.set(stdio_name_settings.user_id)
    client_token = client_name_var.set(stdio_name_settings.client_name)

    try:
        mcp.run(transport="stdio")
    finally:
        user_id_var.reset(user_token)
        client_name_var.reset(client_token)

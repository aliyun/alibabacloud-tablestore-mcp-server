import json
from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import Any, List
from contextlib import AsyncExitStack
import asyncio

import chunk
from config import *
import sys

class MCPClient:
    """
    A client class for interacting with the MCP (Model Control Protocol) server.
    This class manages the connection and communication with the SQLite database through MCP.
    """

    def __init__(self, host: str):
        """Initialize the MCP client with server parameters"""
        self.host = host
        self.exit_stack = AsyncExitStack()
        self.session = None
        self._client = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.__aexit__(exc_type, exc_val, exc_tb)
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def connect(self):
        """Establishes connection to MCP server"""
        self._client = sse_client(self.host, timeout=10)
        stdio_transport = await self.exit_stack.enter_async_context(self._client)
        read, write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))

    async def get_available_tools(self) -> List[Any]:
        """
        Retrieve a list of available tools from the MCP server.
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        tools = await self.session.list_tools()
        return tools.tools

    def call_tool(self, tool_name: str, args) -> Any:
        """
        Create a callable function for a specific tool.
        This allows us to execute database operations through the MCP server.

        Args:
            tool_name: The name of the tool to create a callable for

        Returns:
            A callable async function that executes the specified tool
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        return self.session.call_tool(tool_name, args)


async def agent_loop(mcp_client, query: str, tools, messages: List[dict] = None):
    """
    Main interaction loop that processes user queries using the LLM and available tools.

    This function:
    1. Sends the user query to the LLM with context about available tools
    2. Processes the LLM's response, including any tool calls
    3. Returns the final response to the user

    Args:
        query: User's input question or command
        tools: Dictionary of available database tools and their schemas
        messages: List of messages to pass to the LLM, defaults to None
    """
    available_tools = [{
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema
        }
    } for tool in tools]

    messages = [
        {
            "role": "user",
            "content": query
        }
    ]

    # Query LLM with the system prompt, user query, and available tools
    response = await llm_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=available_tools
    )

    final_text = []
    message = response.choices[0].message
    final_text.append(message.content or "")

    while message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            result = await mcp_client.call_tool(tool_name, tool_args)
            final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

            messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(tool_args)
                        }
                    }
                ]
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result.content)
            })

        response = await llm_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            tools=available_tools
        )

        message = response.choices[0].message
        if message.content:
            final_text.append(message.content)

    return "\n".join(final_text)


async def import_knowledge(path):
    knowledge_text = open(path, 'r').read()
    chunks = chunk.to_chunks(knowledge_text, 2000)
    async with MCPClient(MCP_SERVER_HOST) as mcp_client:
        # Get available database tools and prepare them for the LLM
        tools = await mcp_client.get_available_tools()

        print('Total Chunks: %d' % len(chunks))
        i = 0
        for c in chunks:
            print('Processing chunk %d.' % i)
            i = i + 1
            query = analysis_content_prompt_template % c
            response = await agent_loop(mcp_client, query, tools)
            try:
                j = json.loads(response)
            except Exception as e:
                continue

            for kc in j['Chunks']:
                q = store_knowledge_prompt_template % kc
                response = await agent_loop(mcp_client, q, tools)
                print(response)

            for faq in j['FAQs']:
                q = store_faq_prompt_template % (faq['Question'], faq['Answer'])
                response = await agent_loop(mcp_client, q, tools)
                print(response)

async def search_knowledge(query):
    query = search_prompt_template % query
    async with MCPClient(MCP_SERVER_HOST) as mcp_client:
        # Get available database tools and prepare them for the LLM
        tools = await mcp_client.get_available_tools()
        response = await agent_loop(mcp_client, query, tools)
        print(response)

async def chat(query):
    query = chat_prompt_template % query
    async with MCPClient(MCP_SERVER_HOST) as mcp_client:
        # Get available database tools and prepare them for the LLM
        tools = await mcp_client.get_available_tools()
        response = await agent_loop(mcp_client, query, tools)
        print(response)

async def main():
    # read args from sys.args, return error if args count less than 2
    if len(sys.argv) != 3:
        print("Usage: python knowledge_manager.py import/search/chat <args>")
        return

    command = sys.argv[1]
    args = sys.argv[2]

    if command == 'import':
        await import_knowledge(args)
    elif command == 'search':
        await search_knowledge(args)
    elif command == 'chat':
        await chat(args)
    else:
        print("Usage: python knowledge_manager.py import/search/chat <args>")
        return

if __name__ == "__main__":
    asyncio.run(main())
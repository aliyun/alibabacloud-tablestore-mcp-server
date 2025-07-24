import argparse

from fastapi import FastAPI
from tablestore_openmemory_mcp.mcp_server import setup_mcp_server, run_stdio
from fastapi.middleware.cors import CORSMiddleware
from tablestore_openmemory_mcp.settings import ServerSettings
import uvicorn

import logging


def parse_args():
    parser = argparse.ArgumentParser(description="tablestore-mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
    )
    return parser.parse_args()


def start_sse_mcp_server():
    server_settings = ServerSettings()

    app = FastAPI(title="OpenMemory API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup MCP server
    setup_mcp_server(app)

    uvicorn.run(app, host=server_settings.host, port=server_settings.port)


def start_stdio_mcp_server():
    run_stdio()


transport2start_func = {
    "sse": start_sse_mcp_server,
    "stdio": start_stdio_mcp_server,
}


def start_mcp_server(transport: str = "sse"):
    if transport not in transport2start_func.keys():
        logging.exception(f"transport {transport} is not supported.")
        raise Exception(f"transport {transport} is not supported.")

    transport2start_func[transport]()


def main():
    args = parse_args()
    start_mcp_server(args.transport)


if __name__ == "__main__":
    main()

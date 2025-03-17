import argparse
import logging

logging.basicConfig(level=logging.INFO)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="tablestore-mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
    )
    args = parser.parse_args()

    # 所有的配置都来自环境变量
    from tablestore_mcp_server.server import mcp

    logging.info(f"run tablestore-mcp-server by: {args.transport}")
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()

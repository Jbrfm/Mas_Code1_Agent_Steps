"""Expose the project's two tools over MCP stdio (slides 15–17)."""

from mcp.server.fastmcp import FastMCP

from .tools import add, get_weather

mcp = FastMCP("basic-agent-tools")
mcp.tool()(add)
mcp.tool()(get_weather)


def main() -> None:
    # stdout belongs to the MCP protocol; send diagnostics to stderr.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

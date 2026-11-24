"""Expose the project's tools over MCP stdio (slides 15–17)."""

from mcp.server.fastmcp import FastMCP

from .tools import add, analyze_csv, analyze_text, get_weather

mcp = FastMCP("basic-agent-tools")
mcp.tool()(add)
mcp.tool()(get_weather)
mcp.tool()(analyze_text)
mcp.tool()(analyze_csv)


def main() -> None:
    # stdout belongs to the MCP protocol; send diagnostics to stderr.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

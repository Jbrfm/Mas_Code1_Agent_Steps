"""Integration checks against a real MCP subprocess; no API key required."""

import unittest

from basic_agent.main import create_mcp_client


class MCPToolsTest(unittest.IsolatedAsyncioTestCase):
    async def test_discovery_and_calls(self) -> None:
        client = create_mcp_client()
        async with client.session("basic") as session:
            listing = await session.list_tools()
            schemas = {tool.name: tool.inputSchema for tool in listing.tools}
            self.assertEqual(set(schemas), {"add", "get_weather"})
            self.assertEqual(schemas["add"]["properties"]["a"]["type"], "integer")
            self.assertEqual(schemas["get_weather"]["required"], ["city"])
            for name, args, expected in [
                ("add", {"a": 47832, "b": 91347}, "139179"),
                ("get_weather", {"city": "Paris"}, "sunny, 22°C"),
                ("get_weather", {"city": "LONDON"}, "rainy, 14°C"),
                ("get_weather", {"city": "Tehran"}, "unknown city"),
            ]:
                with self.subTest(name=name, args=args):
                    result = await session.call_tool(name, args)
                    self.assertFalse(result.isError)
                    self.assertEqual(result.content[0].text, expected)
            invalid = await session.call_tool("add", {"a": "invalid", "b": 1})
            self.assertTrue(invalid.isError)

        tools = {tool.name: tool for tool in await client.get_tools()}
        result = await tools["add"].ainvoke({"a": 47832, "b": 91347})
        self.assertIn("139179", str(result))


if __name__ == "__main__":
    unittest.main()

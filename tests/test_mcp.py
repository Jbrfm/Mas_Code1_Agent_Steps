"""Integration checks against a real MCP subprocess; no API key required."""

import unittest
import json

from basic_agent.main import create_mcp_client


class MCPToolsTest(unittest.IsolatedAsyncioTestCase):
    async def test_discovery_and_calls(self) -> None:
        client = create_mcp_client()
        async with client.session("basic") as session:
            listing = await session.list_tools()
            schemas = {tool.name: tool.inputSchema for tool in listing.tools}
            self.assertEqual(set(schemas), {"add", "get_weather", "analyze_text", "analyze_csv"})
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
            text = await session.call_tool("analyze_text", {"text": "Hello MCP! Hello."})
            self.assertFalse(text.isError)
            self.assertEqual(json.loads(text.content[0].text)["word_count"], 3)
            csv = await session.call_tool("analyze_csv", {"csv_text": "score\n18\n20\n16"})
            self.assertFalse(csv.isError)
            self.assertEqual(json.loads(csv.content[0].text)["columns"]["score"]["mean"], 18)
            malformed = await session.call_tool("analyze_csv", {"csv_text": "a,b\n1"})
            self.assertTrue(malformed.isError)

        tools = {tool.name: tool for tool in await client.get_tools()}
        result = await tools["add"].ainvoke({"a": 47832, "b": 91347})
        self.assertIn("139179", str(result))


if __name__ == "__main__":
    unittest.main()

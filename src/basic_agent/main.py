import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from .tools import add, get_weather

# Read configuration from the project root.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        raise SystemExit("Add your Groq API key to OPENAI_API_KEY in .env first.")

    llm = ChatOpenAI(
        model=os.getenv("MODEL", "openai/gpt-oss-20b"),
        temperature=0,
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1"),
        api_key=api_key,
        timeout=30,
        max_retries=0,
    )
    agent = create_agent(llm, [add, get_weather])
    result = agent.invoke(
        {
            "messages": [
                ("user", "Use the add tool for 47832 + 91347, and get_weather for Paris.")
            ]
        },
        config={"recursion_limit": 10},
    )
    for msg in result["messages"]:
        print(f"[{msg.type}] {msg.content}")
        for tc in getattr(msg, "tool_calls", None) or []:
            print(f"   -> {tc['name']}({tc['args']})")


if __name__ == "__main__":
    main()

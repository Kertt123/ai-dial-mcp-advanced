import asyncio
import os
from typing import Any

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.dial_client import DialClient
from agent.models.message import Message, Role


async def main():
    api_key = os.getenv("DIAL_API_KEY")
    if not api_key:
        raise RuntimeError("DIAL_API_KEY environment variable is required")

    tools: list[dict[str, Any]] = []
    tool_name_client_map: dict[str, MCPClient | CustomMCPClient] = {}

    ums_client = await CustomMCPClient.create("http://localhost:8006/mcp")
    ums_tools = await ums_client.get_tools()
    tools.extend(ums_tools)
    for tool in ums_tools:
        tool_name_client_map[tool["function"]["name"]] = ums_client

    remote_client = await MCPClient.create("https://remote.mcpservers.org/fetch/mcp")
    remote_tools = await remote_client.get_tools()
    tools.extend(remote_tools)
    for tool in remote_tools:
        tool_name_client_map[tool["function"]["name"]] = remote_client

    dial_client = DialClient(
        api_key=api_key,
        endpoint="https://ai-proxy.lab.epam.com",
        tools=tools,
        tool_name_client_map=tool_name_client_map
    )

    messages = [
        Message(
            role=Role.SYSTEM,
            content="You are a helpful assistant that uses MCP tools to manage UMS users and external data."
        )
    ]

    print("Type 'exit' or 'quit' to leave the chat.")

    while True:
        user_input = (await asyncio.to_thread(input, "👤: ")).strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Kończę pracę. Do zobaczenia!")
            break
        if not user_input:
            continue

        messages.append(Message(role=Role.USER, content=user_input))

        try:
            ai_message = await dial_client.get_completion(messages)
            messages.append(ai_message)
            if ai_message.content:
                print(f"🤖: {ai_message.content}")
        except Exception as exc:
            error_msg = f"Błąd podczas obsługi zapytania: {exc}"
            print(error_msg)
            messages.append(Message(role=Role.AI, content=error_msg))


if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him
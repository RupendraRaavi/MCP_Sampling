import asyncio
from fastmcp import Client
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext

async def sampling_handler(messages: list[SamplingMessage], params: SamplingParams, context: RequestContext) -> str:
    
    convo = []
    for m in messages:
        content = getattr(m.content, "text", m.content) if hasattr(m, "content") else str(m)
        convo.append(f"{m.role}: {content}")
    return " | ".join(convo) + "  -- (handled by client sampling_handler)"

async def main():
    client = Client("welcome_server.py", sampling_handler=sampling_handler)

    async with client:
        tools = await client.list_tools()
        print("tools/list ->", tools)

        res = await client.call_tool(
            "generate_welcome_note_options",
            {"topic": "a product manager joining our startup"},
        )
        print("tools/call ->", res.data)

if __name__ == "__main__":
    asyncio.run(main())

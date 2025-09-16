import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext
from openai import AsyncOpenAI 

load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def sampling_handler(messages: list[SamplingMessage], params: SamplingParams, context: RequestContext) -> str:
    """
    Client-side sampling handler — this is called when the server requests sampling.
    It calls the client's preferred LLM and returns a candidate string.
    """
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    openai_messages = []
    if params.systemPrompt:
        openai_messages.append({"role": "system", "content": params.systemPrompt})

    for m in messages:
        content = getattr(m.content, "text", m.content) if hasattr(m, "content") else str(m)
        openai_messages.append({"role": m.role, "content": content})

    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=openai_messages,
        temperature=0.8,
        max_tokens=300,
        n=1,
    )

    if resp.choices:
        return resp.choices[0].message.content.strip()

    return ""

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

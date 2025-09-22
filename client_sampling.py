import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext
from openai import AsyncOpenAI 

load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def sampling_handler(messages: list[SamplingMessage], params: SamplingParams, context: RequestContext) -> str:
    
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
        max_tokens=500,
        n=3,
    )

    if resp.choices:
        return resp.choices[0].message.content.strip()

    return ""

async def main():
  
    client = Client("agent_server.py", sampling_handler=sampling_handler)

    async with client:
        print("--- Calling welcome tool ---")
        user_topic = input("Enter your topic ")
        welcome_res = await client.call_tool(
            "generate_welcome_note_options",
            {"topic": user_topic},
        )
        print(welcome_res.data)

        print("--- Calling expander tool ---")
        user_goal = input("Enter your goal ")
        expander_res = await client.call_tool(
            "expander",
            {"goal": user_goal},
        )
        print(expander_res.data)

        print("\n--- Calling get_blood_test_results tool ---")
        name = input("Enter your name: ")                                                                                          
        hemoglobin = input("Enter your hemoglobin level (e.g., 15.5 g/dL): ")                                                      
        cholesterol = input("Enter your cholesterol level (e.g., 190 mg/dL): ")                                                    
        glucose = input("Enter your glucose level (e.g., 130 mg/dL): ") 
        blood_test_res = await client.call_tool(
            "get_blood_test_results",
            {                                                                                                                      
                "name": name,                                                                                                      
                "hemoglobin": hemoglobin,                                                                                          
                "cholesterol": cholesterol,                                                                                        
                "glucose": glucose,                                                                                                
            },
        )
        print(blood_test_res.data)

if __name__ == "__main__":
    asyncio.run(main())

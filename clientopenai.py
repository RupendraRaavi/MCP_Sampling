import asyncio
import random
from fastmcp import Client

async def main():
    print("Connecting to server...")
    client = Client("welcome_server.py")

    async with client:
        tools = await client.list_tools()
        print("\n--- Available Tools ---")
        for tool in tools:
            print(f"- {tool.name}")

        print("\n--- Generating Welcome Note Options ---")
        topic = "a product manager joining our startup"
        print(f"Topic: {topic}")
        
        res = await client.call_tool(
            "generate_welcome_note_options",
            {"topic": topic},
        )
        
        options = res.data
        print("\n--- Received Options ---")
        if not options or not isinstance(options, list):
            print("Failed to receive valid options.")
            return

        for i, option in enumerate(options):
            print(f"Option {chr(65 + i)}:\n{option}\n")

        if len(options) > 1:
            chosen_option_index = random.randint(0, len(options) - 1) 
            chosen_option = options[chosen_option_index]
            print(f"--- User's Choice ---")
            print(f"User selected Option {chr(65 + chosen_option_index)}.")
            print(f"Workflow continues with text: \"{chosen_option}\"")
        elif options:
            print("--- User's Choice ---")
            print("Only one option was generated, proceeding with that one.")
            print(f"Workflow continues with text: \"{options[0]}\"")


if __name__ == "__main__":
    asyncio.run(main())

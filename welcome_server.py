import re
from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from mcp import McpError

load_dotenv()

mcp = FastMCP(
    name="WelcomeNotesServer",
)

@mcp.tool
async def generate_welcome_note_options(ctx: Context, topic: str = "a new team member") -> list[str]:
    """
    Generates three distinct welcome notes for a given topic.
    """
    system_prompt = (
        "You are an expert in writing short welcome notes. "
        "Produce exactly three distinct welcome notes for the topic given by the user. "
        "Number each option (1., 2., 3.). Keep each option between 1 and 6 sentences and vary tone and length."
    )
    user_message = f"Topic: {topic}\nReturn three numbered options."

    try:
        response = await ctx.sample(
            messages=[user_message],
            system_prompt=system_prompt,
        )
        raw = getattr(response, "text", "") or ""
        # Split the response by numbered list format (e.g., "1.", "2.")
        parts = re.split(r"\n\s*(?:\d+\.)\s*", raw)
        # Filter out any empty strings that result from splitting
        parts = [p.strip() for p in parts if p.strip()]
        
        if not parts:
            return ["Sorry — no generated options available."]
        
        return parts

    except McpError as e:
        error_message = e.error if hasattr(e, 'error') else str(e)
        return [f"An error occurred during sampling: {error_message}"]

if __name__ == "__main__":
    mcp.run()
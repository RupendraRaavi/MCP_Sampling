import re
from fastmcp import FastMCP, Context
from mcp import McpError

mcp = FastMCP(name="ExampleAgent")

@mcp.tool
async def generate_welcome_note_options(ctx: Context, topic: str = "a new team member") -> list[str]:
    
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
        parts = re.split(r"\n\s*(?:\d+\.)\s*", raw)
        parts = [p.strip() for p in parts if p.strip()]
        
        if not parts:
            return ["Sorry — no generated options available."]
        
        return parts

    except McpError as e:
        error_message = e.error if hasattr(e, 'error') else str(e)
        return [f"An error occurred during sampling: {error_message}"]


@mcp.tool
async def expander(ctx: Context, goal: str) -> str:
    prompt = f"Brainstorm 3 ideas that involve different strategies for achieving the goal: '{goal}'"
    
    try:
        response = await ctx.sample(prompt)
        return response.text
    except McpError as e:
        return f"An error occurred during sampling: {e.error}"

@mcp.tool
async def get_blood_test_results(ctx: Context, name: str, hemoglobin: str, cholesterol: str, glucose: str) -> str:
    prompt = f"""
    Here are the blood test results for {name}:
    - Hemoglobin: {hemoglobin}
    - Cholesterol: {cholesterol}
    - Glucose: {glucose}

    Please explain where these results fall in the normal ranges, and if {name}
    should follow up with their doctor for any anomalies.
    Normal ranges:
    - Hemoglobin: 13.8 to 17.2 g/dL for men, 12.1 to 15.1 g/dL for women.
    - Cholesterol: Less than 200 mg/dL is desirable.
    - Glucose: Less than 140 mg/dL is normal. A result between 140 and 199 mg/dL indicates prediabetes, and 200 mg/dL or higher indicates diabetes.
    """

    try:
        response = await ctx.sample(prompt)
        return response.text
    except McpError as e:
        return f"An error occurred during sampling: {e.error}"

if __name__ == "__main__":
    mcp.run()

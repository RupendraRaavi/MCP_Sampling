import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

WELCOME_SERVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'welcome_server.py'))

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='welcome_agent',
    instruction='You are a helpful agent that can generate welcome notes.',
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='python',
                    args=[
                        WELCOME_SERVER_PATH,
                    ],
                ),
            ),
        )
    ],
)

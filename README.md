# MCP Sampling

This project demonstrates a client-server setup using `fastmcp` where a server exposes multiple tools and a client calls them, handling the LLM sampling itself. It also includes an example of how to integrate the MCP server as a tool within a Google ADK agent.

## Overview

This project contains a `fastmcp` server that exposes three tools:

1.  `generate_welcome_note_options`: Generates welcome notes for a given topic.
2.  `expander`: Brainstorms ideas to achieve a specified goal.
3.  `get_blood_test_results`: Analyzes mock blood test results and provides an explanation.

A "thick" client (`client_sampling.py`) connects to this server, calls the tools, and uses its own `sampling_handler` to process the LLM requests with the OpenAI API.

Additionally, it includes an example of how to integrate the MCP server as a tool within a Google ADK agent (`sampling_agent/agent.py`).

## File Structure

-   `agent_server.py`: The `FastMCP` server. It exposes the `generate_welcome_note_options`, `expander`, and `get_blood_test_results` tools.
-   `client_sampling.py`: A "thick" client with its own `sampling_handler` that calls the OpenAI API to fulfill sampling requests from the server's tools.
-   `sampling_agent/agent.py`: A Google ADK agent that uses `agent_server.py` as a tool.
-   `.env`: An environment file to store your API key.

## Prerequisites

-   Python 3.10+
-   An OpenAI API key.

## Setup

1.  **Set up the Python Virtual Environment:**
    From the project root directory, run:
    ```bash
    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # On Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

2.  **Install Dependencies:**
    Install the required Python packages.
    ```bash
    pip install fastmcp "fastmcp[openai]" python-dotenv google-adk openai
    ```

3.  **Configure your OpenAI API Key:**
    Create a file named `.env` in the root directory and add your OpenAI API key to it.
    ```ini
    # .env
    OPENAI_API_KEY="sk-..."
    ```

## Running the Examples

Make sure your virtual environment is activated for all examples.

### Example 1: Client-Side Sampling (Thick Client)

This test uses `client_sampling.py` and demonstrates the client performing the LLM completion for the tools on the server.

1.  Ensure your `.env` file contains a valid `OPENAI_API_KEY`.
2.  Run the script from your terminal:
    ```bash
    python client_sampling.py
    ```
**Expected Output:** The script will connect to the server (which is started automatically). It will then prompt you for input for each of the three tools (`generate_welcome_note_options`, `expander`, and `get_blood_test_results`) and print the AI-generated responses.

### Example 2: Google ADK Agent Integration

This test runs the `agent_server` as a tool within an ADK agent.

**Important:** For this example to work, you must first modify `agent_server.py` to include a fallback sampling handler. The ADK agent does not provide a sampling handler, so the server must have its own to process LLM requests. You can copy the `sampling_handler` function and related imports (like `os`, `AsyncOpenAI`, etc.) from `client_sampling.py` into `agent_server.py` and register it with the `FastMCP` instance (e.g., `mcp = FastMCP(name="ExampleAgent", fallback_sampling_handler=sampling_handler)`).

1.  Ensure your `.env` file contains a valid `OPENAI_API_KEY`.
2.  Run the ADK web server from your terminal:
    ```bash
    adk serve -a sampling_agent/agent.py
    ```
3.  Open the URL provided by the command (e.g., `http://127.0.0.1:8080`) in your web browser.
4.  In the chat interface, ask the agent to use one of the tools. For example:
    > "generate welcome notes for a new intern"
    > "brainstorm ideas for improving team morale"
    > "analyze these blood test results for John Doe: hemoglobin 16 g/dL, cholesterol 180 mg/dL, glucose 120 mg/dL"

**Expected Output:** The agent will use its MCP tool to connect to the `agent_server.py` and display the AI-generated responses in the chat interface.

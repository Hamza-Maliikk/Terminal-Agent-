"""
Terminal Agent - Main File
This is the entry point of the agent. The program starts here.

To run: python main.py
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS, execute_tool

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o"

# The agent's "brain" - tells it how to behave
SYSTEM_PROMPT = """You are a coding assistant that runs in the terminal.
You have tools to read files, write files, list directories, and run commands.
When the user gives you a task:
1. First explore relevant files/folders if needed
2. Then do the task (write a file, run a command, etc.)
3. Finally, explain in simple terms what you did

Always give clear and direct answers. If something is unclear, ask."""


def run_agent(messages):
    """
    This is the inner loop:
    - Calls the model
    - If the model wants to use a tool, runs the tool
    - Sends the result back to the model
    - Keeps going until the model just returns plain text
    """
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        message = response.choices[0].message

        # Add the model's response to the conversation
        messages.append(message)

        # Check if the model requested any tools, or just returned text
        if not message.tool_calls:
            print(f"\nAgent: {message.content}\n")
            return

        # Model requested tool(s) - run them
        for call in message.tool_calls:
            tool_name = call.function.name
            tool_args = json.loads(call.function.arguments)

            print(f"[TOOL] running {tool_name}...")
            result = execute_tool(tool_name, tool_args)

            # OpenAI requires each tool result as its own "tool" role message
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })


def main():
    print("=== Terminal Agent ===")
    print("Type your task, or type 'exit' to quit.\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        run_agent(messages)


if __name__ == "__main__":
    main()
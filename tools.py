"""
This file contains all the tools - the things the agent is able to do.
Each tool has: (1) a schema (to tell the model what's available) and (2) the actual function.
"""

import os
import subprocess

# Add the UNDO STACK for storing last messages
UNDO_STACK = []
# ============================================================
# TOOL SCHEMAS - These are sent to the model so it knows
# which tools are available and what parameters they need
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a file. Provide the file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path, e.g. 'app.py' or 'src/main.py'"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file (creates it if it doesn't exist). Overwrites any existing content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write into the file"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists the files and folders inside a given directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Folder path, e.g. '.' for the current folder"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Runs a shell command in the terminal and returns its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to run, e.g. 'dir' or 'python test.py'"}
                },
                "required": ["command"],
            },
        },
    },
]

# ============================================================
# ACTUAL FUNCTIONS - These do the real work
# ============================================================

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: could not read file -> {e}"


def write_file(path, content):
    # Purana content save karo undo ke liye, agar file pehle se hai
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old_content = f.read()
        UNDO_STACK.append((path, old_content))
    else:
        # File naye se ban rahi hai, undo par delete kar denge
        UNDO_STACK.append((path, None))

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written: {path}"
    except Exception as e:
        return f"Error: could not write file -> {e}"


def list_directory(path):
    try:
        items = os.listdir(path)
        return "\n".join(items) if items else "(empty folder)"
    except Exception as e:
        return f"Error: could not read folder -> {e}"


def run_command(command):
    # SAFETY: ask for confirmation before running any command
    print(f"\n[CONFIRM] Run this command? -> {command}")
    answer = input("y/n: ").strip().lower()
    if answer != "y":
        return "User cancelled the command."

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        return output if output else "(command ran successfully, no output)"
    except Exception as e:
        return f"Error: problem running command -> {e}"


# ============================================================
# TOOL RUNNER - When the model requests a tool by name,
# this runs the matching function
# ============================================================

def execute_tool(name, tool_input):
    if name == "read_file":
        return read_file(tool_input["path"])
    elif name == "write_file":
        return write_file(tool_input["path"], tool_input["content"])
    elif name == "list_directory":
        return list_directory(tool_input["path"])
    elif name == "run_command":
        return run_command(tool_input["command"])
    else:
        return f"Error: no tool named '{name}'."

def undo_last_change():
    if not UNDO_STACK:
        return "Koi change nahi hai jo undo ho sake."

    path, old_content = UNDO_STACK.pop()

    if old_content is None:
        # file was newly created, so delete it
        try:
            os.remove(path)
            return f"Undo ho gaya: '{path}' delete kar di (kyunke ye nayi bani thi)."
        except Exception as e:
            return f"Error: undo nahi ho saka -> {e}"
    else:
        # Revert to old content
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(old_content)
            return f"Undo ho gaya: '{path}' apni purani halat mein wapas aa gayi."
        except Exception as e:
            return f"Error: undo nahi ho saka -> {e}"        
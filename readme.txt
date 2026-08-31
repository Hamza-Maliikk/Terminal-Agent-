# Terminal Agent

A lightweight AI coding agent that runs directly in your terminal. It can read files, write files, list directories, and run shell commands — all guided by natural language instructions. Powered by OpenAI's GPT models.

Think of it as a minimal version of tools like Claude Code or Codex CLI: you type what you want, and the agent figures out which actions to take.

## Features

- **Natural language control** — just describe what you want, no special syntax needed
- **File operations** — read, write, and list files/folders on your behalf
- **Shell command execution** — runs terminal commands with your confirmation before anything happens
- **Safety confirmation** — every shell command asks for a `y/n` before running, so nothing destructive happens without your approval
- **Undo support** — reverse the last file change with a single `undo` command
- **Simple, minimal codebase** — just two Python files, easy to read and extend

## How It Works

The agent runs a loop:

1. You type a request in the terminal
2. The request is sent to the OpenAI model, along with a list of available tools
3. The model decides whether it needs to use a tool (e.g. read a file, run a command) or just reply with text
4. If a tool is needed, the agent runs it locally and sends the result back to the model
5. This repeats until the model has everything it needs and gives you a final answer

## File Structure

```
terminal-agent/
├── main.py           # Entry point — runs the agent loop and handles user input
├── tools.py          # All available tools (read_file, write_file, list_directory, run_command, undo)
├── .env               # Your OpenAI API key goes here (never shared/committed)
├── .gitignore          # Files and folders Git should ignore
├── requirements.txt   # Python libraries required to run the project
└── README.md           # You're reading it
```

## Setup

1. **Clone or download this project**, then open a terminal inside the folder:
   ```
   cd terminal-agent
   ```

2. **(Optional but recommended) Create a virtual environment:**
   ```
   python -m venv .venv
   ```
   Activate it:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Add your API key.** Open `.env` and replace the placeholder:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxx
   ```
   Get a key from: https://platform.openai.com/api-keys

5. **Run the agent:**
   ```
   python main.py
   ```

## Usage

Once running, just type what you need:

```
You: list the files in this folder
You: read main.py and explain what it does
You: create a file called notes.txt with "hello world" in it
You: run the command dir
```

If the agent tries to run a shell command, it will pause and ask for confirmation:
```
[CONFIRM] Run this command? -> dir
y/n:
```

**To undo the last file change:**
```
You: undo
```
This reverses the most recent `write_file` action. If the file was newly created, `undo` deletes it. If it overwrote an existing file, `undo` restores the previous content. Undo history only lasts for the current session — it resets when you close the program.

**To quit:**
```
You: exit
```

## Available Tools

| Tool | What it does |
|---|---|
| `read_file` | Reads and returns the contents of a file |
| `write_file` | Writes/overwrites content in a file (creates it if missing) |
| `list_directory` | Lists files and folders in a given path |
| `run_command` | Runs a shell command (asks for confirmation first) |
| `undo` (manual command) | Reverses the last file change |

## Notes & Limitations

- This is a simple/educational build — not meant for production use.
- Requires an OpenAI account with billing enabled; otherwise API calls will fail with a quota error.
- The default model is `gpt-4o`, set in `main.py` (`MODEL` variable). Change it if you want a different or cheaper model, e.g. `gpt-4o-mini`.
- Undo only works for file writes, and only for the single most recent change — it is not a full version history.
- Shell commands run with a 30-second timeout and always require manual confirmation.

## Possible Improvements

- Multi-step undo (a full history instead of just the last change)
- Persistent undo history saved to disk
- Colored/formatted terminal output
- Support for additional tools like `search_code` or `delete_file`
- Streaming responses instead of waiting for the full reply
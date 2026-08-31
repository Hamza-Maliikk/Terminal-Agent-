# Terminal Agent

A lightweight AI coding agent that runs directly in your terminal.
It can read files, write files, list directories, and run shell commands — all guided by plain natural language instructions. Powered by OpenAI's GPT models.

Think of it as a minimal version of tools like **Claude Code** or **Codex CLI**: you type what you want, and the agent figures out which actions to take.

---

##  Features

- **Natural language control** — just describe what you want, no special syntax needed
- **File operations** — read, write, and list files/folders on your behalf
- **Shell command execution** — runs terminal commands, always with your confirmation first
- **Safety confirmation** — every shell command asks `y/n` before running, so nothing destructive happens without approval
- **Undo support** — reverse the last file change with a single `undo` command
- **Minimal codebase** — just two Python files, easy to read and extend

---

##  How It Works

The agent runs a simple loop:

1. You type a request in the terminal
2. The request is sent to the OpenAI model, along with a list of available tools
3. The model decides: use a tool (read a file, run a command) — or just reply with text
4. If a tool is needed, the agent runs it locally and sends the result back to the model
5. This repeats until the model has everything it needs and gives a final answer

---

##  File Structure

| File | Purpose |
|---|---|
| `main.py` | Entry point — runs the agent loop and handles user input |
| `tools.py` | All available tools (`read_file`, `write_file`, `list_directory`, `run_command`, `undo`) |
| `.env` | Your OpenAI API key goes here (never shared or committed) |
| `.gitignore` | Files and folders Git should ignore |
| `requirements.txt` | Python libraries required to run the project |
| `README.md` | This file |

---

##  Setup

**1. Open a terminal inside the project folder**
```
cd terminal-agent
```

**2. (Optional but recommended) Create a virtual environment**
```
python -m venv .venv
```
Activate it:
- Windows → `.venv\Scripts\activate`
- Mac/Linux → `source .venv/bin/activate`

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Add your API key**

Open `.env` and replace the placeholder:
```
OPENAI_API_KEY=sk-xxxxxxxxxx
```
Get a key here → https://platform.openai.com/api-keys

**5. Run the agent**
```
python main.py
```

---

##  Usage

Once running, just type what you need:

```
You: list the files in this folder
You: read main.py and explain what it does
You: create a file called notes.txt with "hello world" in it
You: run the command dir
```

If the agent tries to run a shell command, it pauses for confirmation:
```
[CONFIRM] Run this command? -> dir
y/n:
```

**Undo the last file change:**
```
You: undo
```
- If the file was newly created → `undo` deletes it
- If it overwrote an existing file → `undo` restores the previous content
- Undo history only lasts for the current session and resets when you close the program

**Quit the agent:**
```
You: exit
```

---

##  Available Tools

| Tool | What it does |
|---|---|
| `read_file` | Reads and returns the contents of a file |
| `write_file` | Writes/overwrites content in a file (creates it if missing) |
| `list_directory` | Lists files and folders in a given path |
| `run_command` | Runs a shell command (asks for confirmation first) |
| `undo` *(manual command)* | Reverses the last file change |

---

##  Notes & Limitations

- This is a simple/educational build — not meant for production use
- Requires an OpenAI account with billing enabled, otherwise API calls fail with a quota error
- Default model is `gpt-4o`, set in `main.py` (`MODEL` variable) — change it for something cheaper like `gpt-4o-mini`
- Undo only reverses the single most recent file write — it's not a full version history
- Shell commands run with a 30-second timeout and always require manual confirmation

---

##  Possible Improvements

- Multi-step undo (full history instead of just the last change)
- Persistent undo history saved to disk
- Colored/formatted terminal output
- Additional tools like `search_code` or `delete_file`
- Streaming responses instead of waiting for the full reply

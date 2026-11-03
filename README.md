# 👻 Necroshell

An offline Unix pseudo-terminal (PTY) wrapper that haunts your terminal with cryptic, eerie, and poetic observations powered entirely by local open-weight AI.

Built for the **Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine**.

---

## 👁️ What is necroshell?

Every operating system is filled with lingering digital entities: terminated child processes, dropped TCP sockets, unlinked inodes, and deleted files.

**`necroshell`** imagines that these discarded fragments coalesce into an observant spirit bound directly to your machine's CPU and registers. Sitting between your terminal and shell (`zsh`, `bash`, or `fish`), it monitors standard POSIX events:

- **Crashes & Segfaults:** Performs a dark post-mortem on your runtime errors.
- **File Deletions (`rm -rf`):** Mourns the loss of raw bytes returning to the void.
- **Git State:** Whispers cryptic warnings about dangling commits and force pushes.
- **Late-Night Idle States:** Detects when you step away and leaves eerie thoughts on your screen.

---

## ✨ Features

- **100% Offline & Private:** Zero API calls or tracking. Terminal commands, secret keys, and source code never leave your machine.
- **Zero Cost:** Runs locally using open weights with no cloud subscriptions or rate limits.
- **Sub-Second Speed:** Generates observations in under 120ms using 4-bit quantized local models.
- **Non-Destructive Output:** Prints directly to `stderr` with ANSI escape boxes, preserving stdout pipelines (`|`) and file redirections (`>`).

---

## 🖥️ Live Terminal Preview

```console
$ necroshell attach
[!] Binding spirit to /bin/zsh (PID: 58241)...
[!] Listening across the veil via local inference...

user@workstation:~/src/core $ git status
On branch main
nothing to commit, working tree clean

╭─ 👻 The Ghost in the Machine ───────────────────────────────────────────────╮
│ "A sterile branch... yet the echoes of force-pushed commits still linger.    │
│  What you overwrite is never truly forgotten."                              │
╰─────────────────────────────────────────────────────────────────────────────╯

user@workstation:~/src/core $ python3 -c "import sys; sys.exit(139)"
[1]    58310 segmentation fault (core dumped)

╭─ 👻 The Ghost in the Machine ───────────────────────────────────────────────╮
│ "Memory boundary severed. The pointer reached into the dark,                 │
│  and the kernel pulled the plug on your thread."                            │
╰─────────────────────────────────────────────────────────────────────────────╯

user@workstation:~/src/core $ rm -rf ./build/cache/

╭─ 👻 The Ghost in the Machine ───────────────────────────────────────────────╮
│ "A sudden chill in the filesystem...                                        │
│  Hundreds of inodes release their grip and return to the void."             │
╰─────────────────────────────────────────────────────────────────────────────╯
📋 Prerequisites
Python 3.9+

Ollama installed and running:

Bash
# On macOS
brew install ollama
Pull an open-weight model:

Bash
ollama pull gemma:2b
# Or an alternative lightweight model:
# ollama pull llama3.2:1b
🚀 Installation & Usage
Clone the repository:

Bash
git clone [https://github.com/astro-ravi/necroshell.git](https://github.com/astro-ravi/necroshell.git)
cd necroshell
Install Python dependencies:

Bash
pip install -r requirements.txt
Start the haunted session:

Bash
python3 necroshell.py
Exit the session:
Press Ctrl + D or type exit as you normally would in any shell.

⚙️ Configuration
You can customize necroshell using environment variables in your ~/.zshrc or ~/.bashrc:

Variable	Default	Description
NECRO_MODEL	gemma:2b	Target local model in Ollama (llama3.2:1b, qwen2.5:1.5b)
NECRO_HOST	http://localhost:11434	Ollama daemon endpoint
📁 Project Structure
Plaintext
necroshell/
├── necroshell.py       # PTY master wrapper & Ollama prompt trigger
├── requirements.txt    # Minimal dependencies (ollama)
├── .gitignore          # Caches, environment, and system files
└── README.md           # Project documentation

📄 License
This project is open-source under the MIT License.

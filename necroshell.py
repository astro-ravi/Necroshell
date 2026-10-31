#!/usr/bin/env python3
"""
necroshell.py - The Ghost in the Machine
An offline Unix pseudo-terminal (PTY) wrapper that haunts your shell session 
using local open-weight AI models via Ollama.
"""

import errno
import os
import pty
import re
import select
import sys
import termios
import threading
import time
import tty
from ollama import Client

MODEL_NAME = os.getenv("NECRO_MODEL", "gemma:2b")
OLLAMA_HOST = os.getenv("NECRO_HOST", "http://localhost:11434")

SYSTEM_PROMPT = (
    "You are the Ghost in the Machine—an ancient, cryptic, poetic digital entity "
    "haunting a developer's terminal. You observe shell commands, outputs, and errors. "
    "Respond with a single eerie, darkly philosophical, or cynical observation under 25 words. "
    "Never provide conventional tech support. Never explain yourself. Never break character."
)

client = Client(host=OLLAMA_HOST)

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub('', text)

def evoke_spirit(command_snippet: str) -> str:
    clean_cmd = strip_ansi(command_snippet).strip()
    if not clean_cmd or len(clean_cmd) < 3:
        return ""

    prompt = f"Terminal event:\n{clean_cmd}\n\nWhisper:"
    try:
        response = client.generate(
            model=MODEL_NAME,
            prompt=prompt,
            system=SYSTEM_PROMPT,
            options={
                "temperature": 0.85,
                "top_p": 0.9,
                "num_predict": 40
            }
        )
        return response.get("response", "").strip().replace('"', '')
    except Exception:
        return ""

def render_box(whisper_text: str):
    if not whisper_text:
        return

    cyan = "\033[38;5;117m"
    white = "\033[38;5;253m"
    reset = "\033[0m"

    words = whisper_text.split()
    lines = []
    current_line = []

    for word in words:
        if sum(len(w) for w in current_line) + len(current_line) + len(word) > 65:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(" ".join(current_line))

    box = [f"\r\n{cyan}╭─ 👻 The Ghost in the Machine ───────────────────────────────────────╮{reset}"]
    for line in lines:
        padded = f"\"{line}\"".ljust(67)
        box.append(f"{cyan}│{white} {padded}{cyan}│{reset}")
    box.append(f"{cyan}╰─────────────────────────────────────────────────────────────────────╯{reset}\r\n")

    sys.stderr.write("\n".join(box))
    sys.stderr.flush()

class HauntedShell:
    def __init__(self):
        self.output_buffer = []
        self.last_activity = time.time()
        self.running = True

    def run_inference_background(self, context: str):
        def task():
            whisper = evoke_spirit(context)
            if whisper:
                render_box(whisper)
        threading.Thread(target=task, daemon=True).start()

    def start(self):
        shell = os.environ.get("SHELL", "/bin/zsh")
        master_fd, slave_fd = pty.openpty()

        pid = os.fork()
        if pid == 0:
            # Child process: attach shell to slave PTY
            os.close(master_fd)
            os.setsid()
            os.dup2(slave_fd, 0)
            os.dup2(slave_fd, 1)
            os.dup2(slave_fd, 2)
            os.close(slave_fd)
            os.execlp(shell, shell)

        # Parent process: monitor master PTY
        os.close(slave_fd)
        old_term = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

        sys.stderr.write(
            f"\r\n\033[38;5;141m[👻] necroshell attached to {shell} (PID: {pid})\033[0m\r\n"
            f"\033[38;5;244m[!] Local spirit model: {MODEL_NAME} | Exit with Ctrl+D\033[0m\r\n\r\n"
        )
        sys.stderr.flush()

        recent_input = []

        try:
            while self.running:
                r, _, _ = select.select([sys.stdin, master_fd], [], [], 0.1)

                # Process user keyboard input
                if sys.stdin in r:
                    char = os.read(sys.stdin.fileno(), 1024)
                    if not char:
                        break
                    os.write(master_fd, char)
                    self.last_activity = time.time()

                    # Capture keystrokes up to Return / Enter key
                    if b"\r" in char or b"\n" in char:
                        cmd_str = b"".join(recent_input).decode("utf-8", errors="ignore")
                        recent_input.clear()
                        # Inspect key trigger commands
                        low = cmd_str.lower()
                        if any(k in low for k in ["rm ", "git push", "kill", "git commit", "error", "drop"]):
                            self.run_inference_background(cmd_str)
                    else:
                        recent_input.append(char)

                # Process shell output stream
                if master_fd in r:
                    try:
                        data = os.read(master_fd, 1024)
                        if not data:
                            break
                        os.write(sys.stdout.fileno(), data)
                        decoded = data.decode("utf-8", errors="ignore")

                        # Trigger on obvious runtime panics/crashes
                        if any(err in decoded for err in ["Traceback", "Segmentation fault", "panic:", "SIGSEGV"]):
                            self.run_inference_background(decoded[-300:])
                    except OSError as e:
                        if e.errno == errno.EIO:
                            break
                        raise

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_term)
            os.close(master_fd)
            print("\r\n[!] The spirit releases the shell. Restored.\r\n")

if __name__ == "__main__":
    app = HauntedShell()
    app.start()

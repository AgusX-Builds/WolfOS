import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
import datetime
import subprocess
import os
import re
import ast
import operator
import sounddevice as sd
import whisper
import numpy as np

# ============================================================

# WOLF AI

# Voice-controlled AI assistant for WOLF OS

# ============================================================

SAMPLE_RATE = 16000
LISTEN_SECONDS = 3

# ------------------------------------------------------------

# Safe calculator

# ------------------------------------------------------------

OPERATORS = {
ast.Add: operator.add,
ast.Sub: operator.sub,
ast.Mult: operator.mul,
ast.Div: operator.truediv,
ast.Mod: operator.mod,
ast.Pow: operator.pow,
ast.USub: operator.neg,
ast.UAdd: operator.pos,
}

def safe_calculate(expression):
expression = expression.replace("^", "**")
expression = expression.replace("x", "*")
expression = expression.replace("X", "*")

```
try:
    tree = ast.parse(expression, mode="eval")
    return evaluate_node(tree.body)
except Exception:
    return None
```

def evaluate_node(node):
if isinstance(node, ast.Constant):
if isinstance(node.value, (int, float)):
return node.value
raise ValueError()

```
if isinstance(node, ast.BinOp):
    operation = OPERATORS.get(type(node.op))
    if operation is None:
        raise ValueError()

    left = evaluate_node(node.left)
    right = evaluate_node(node.right)

    if isinstance(node.op, ast.Pow) and abs(right) > 100:
        raise ValueError()

    return operation(left, right)

if isinstance(node, ast.UnaryOp):
    operation = OPERATORS.get(type(node.op))
    if operation is None:
        raise ValueError()

    return operation(evaluate_node(node.operand))

raise ValueError()
```

# ------------------------------------------------------------

# WOLF AI

# ------------------------------------------------------------

class WolfAI:

```
def __init__(self, root):
    self.root = root

    self.voice_mode = False
    self.model = None
    self.listening_thread = None

    self.setup_window()
    self.create_interface()

    self.add_message(
        "WOLF",
        "Hello. I am WOLF AI. Say \"WOLF\" followed by a command."
    )

# --------------------------------------------------------
# Window
# --------------------------------------------------------

def setup_window(self):
    self.root.title("WOLF AI")
    self.root.geometry("850x650")
    self.root.minsize(700, 550)
    self.root.configure(bg="#07111F")

# --------------------------------------------------------
# Interface
# --------------------------------------------------------

def create_interface(self):

    header = tk.Frame(
        self.root,
        bg="#07111F"
    )
    header.pack(fill="x", padx=20, pady=(15, 5))

    title = tk.Label(
        header,
        text="🐺 WOLF AI",
        font=("Arial", 26, "bold"),
        fg="white",
        bg="#07111F"
    )
    title.pack(side="left")

    self.status_label = tk.Label(
        header,
        text="● ONLINE",
        font=("Arial", 11, "bold"),
        fg="#39ff88",
        bg="#07111F"
    )
    self.status_label.pack(side="right", pady=8)

    # Chat
    self.chat = scrolledtext.ScrolledText(
        self.root,
        wrap=tk.WORD,
        font=("Arial", 13),
        bg="#0d1b2a",
        fg="white",
        insertbackground="white",
        relief="flat",
        padx=15,
        pady=15
    )

    self.chat.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    self.chat.configure(state="disabled")

    # Bottom area
    bottom = tk.Frame(
        self.root,
        bg="#07111F"
    )
    bottom.pack(fill="x", padx=20, pady=(0, 20))

    self.entry = tk.Entry(
        bottom,
        font=("Arial", 14),
        bg="#16283d",
        fg="white",
        insertbackground="white",
        relief="flat"
    )

    self.entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=12,
        padx=(0, 10)
    )

    self.entry.bind(
        "<Return>",
        lambda event: self.send_text()
    )

    send_button = tk.Button(
        bottom,
        text="SEND",
        font=("Arial", 11, "bold"),
        bg="#1f6feb",
        fg="white",
        activebackground="#388bfd",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=10,
        command=self.send_text
    )

    send_button.pack(side="left", padx=(0, 8))

    self.voice_button = tk.Button(
        bottom,
        text="🎤 WAKE WOLF",
        font=("Arial", 11, "bold"),
        bg="#243447",
        fg="white",
        activebackground="#34495e",
        activeforeground="white",
        relief="flat",
        padx=15,
        pady=10,
        command=self.toggle_voice_mode
    )

    self.voice_button.pack(side="left")

# --------------------------------------------------------
# Chat
# --------------------------------------------------------

def add_message(self, speaker, message):

    self.chat.configure(state="normal")

    self.chat.insert(
        tk.END,
        f"{speaker}: {message}\n\n"
    )

    self.chat.see(tk.END)
    self.chat.configure(state="disabled")

# --------------------------------------------------------
# Text input
# --------------------------------------------------------

def send_text(self):

    text = self.entry.get().strip()

    if not text:
        return

    self.entry.delete(0, tk.END)

    self.add_message("YOU", text)

    response = self.get_response(text)

    self.add_message("WOLF", response)

    self.speak(response)

# --------------------------------------------------------
# Response system
# --------------------------------------------------------

def get_response(self, text):

    original = text
    text = text.lower().strip()

    # Remove common punctuation
    cleaned = re.sub(r"[!?.,]", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # ----------------------------------------------------
    # Greetings
    # ----------------------------------------------------

    if any(word in cleaned for word in [
        "hello",
        "hi",
        "hey",
        "hola"
    ]):
        return "Hello. WOLF AI is online and ready."

    # ----------------------------------------------------
    # Help
    # ----------------------------------------------------

    if "help" in cleaned or "what can you do" in cleaned:
        return (
            "I can tell you the time and date, calculate numbers, "
            "check the battery, open applications and folders, "
            "create notes, open WOLF OS, and control several "
            "parts of your computer."
        )

    # ----------------------------------------------------
    # Time
    # ----------------------------------------------------

    if (
        "what time" in cleaned
        or "current time" in cleaned
        or cleaned == "time"
        or "tell me the time" in cleaned
    ):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    # ----------------------------------------------------
    # Date
    # ----------------------------------------------------

    if (
        "what date" in cleaned
        or "today's date" in cleaned
        or "todays date" in cleaned
        or cleaned == "date"
        or "what day is it" in cleaned
    ):
        current_date = datetime.datetime.now().strftime(
            "%A, %B %d, %Y"
        )
        return f"Today is {current_date}."

    # ----------------------------------------------------
    # Status
    # ----------------------------------------------------

    if "status" in cleaned:
        return (
            "WOLF AI is online. Voice control is "
            + ("active." if self.voice_mode else "inactive.")
        )

    # ----------------------------------------------------
    # Identity
    # ----------------------------------------------------

    if "who are you" in cleaned:
        return (
            "I am WOLF AI, the main artificial intelligence "
            "assistant of WOLF OS."
        )

    if "what are you" in cleaned:
        return "I am WOLF AI, your WOLF OS assistant."

    # ----------------------------------------------------
    # Battery
    # ----------------------------------------------------

    if (
        "battery" in cleaned
        or "battery level" in cleaned
        or "how much battery" in cleaned
    ):
        return self.get_battery()

    # ----------------------------------------------------
    # Calculator
    # ----------------------------------------------------

    calculation = self.extract_calculation(cleaned)

    if calculation:
        result = safe_calculate(calculation)

        if result is not None:
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            return f"The answer is {result}."

    # ----------------------------------------------------
    # Create note
    # ----------------------------------------------------

    if (
        "create note" in cleaned
        or "make a note" in cleaned
        or "write a note" in cleaned
        or "take a note" in cleaned
    ):
        note_text = self.extract_note_text(cleaned)

        if note_text:
            return self.create_note(note_text)

        return "What would you like me to write in the note?"

    # ----------------------------------------------------
    # Open Notes
    # ----------------------------------------------------

    if (
        "open notes" in cleaned
        or "open wolf notes" in cleaned
        or "open my notes" in cleaned
    ):
        self.open_path(
            os.path.expanduser("~/WolfOS/wolf_note.txt")
        )

        return "Opening WOLF Notes."

    # ----------------------------------------------------
    # Open WOLF folder
    # ----------------------------------------------------

    if (
        "open wolf folder" in cleaned
        or "open wolfos folder" in cleaned
        or "open wolf os folder" in cleaned
    ):
        self.open_path(
            os.path.expanduser("~/WolfOS")
        )

        return "Opening the WOLF OS folder."

    # ----------------------------------------------------
    # Open WOLF OS
    # ----------------------------------------------------

    if (
        "open wolf os" in cleaned
        or "launch wolf os" in cleaned
        or "start wolf os" in cleaned
    ):
        self.launch_wolf_os()

        return "Launching WOLF OS."

    # ----------------------------------------------------
    # Applications
    # ----------------------------------------------------

    if "open safari" in cleaned:
        self.open_application("Safari")
        return "Opening Safari."

    if "open finder" in cleaned:
        self.open_application("Finder")
        return "Opening Finder."

    if "open terminal" in cleaned:
        self.open_application("Terminal")
        return "Opening Terminal."

    if "open music" in cleaned:
        self.open_application("Music")
        return "Opening Music."

    if "open calculator" in cleaned:
        self.open_application("Calculator")
        return "Opening Calculator."

    if "open system settings" in cleaned:
        self.open_application("System Settings")
        return "Opening System Settings."

    # ----------------------------------------------------
    # Folders
    # ----------------------------------------------------

    if "open downloads" in cleaned:
        self.open_path(
            os.path.expanduser("~/Downloads")
        )

        return "Opening Downloads."

    if "open desktop" in cleaned:
        self.open_path(
            os.path.expanduser("~/Desktop")
        )

        return "Opening the Desktop."

    if "open documents" in cleaned:
        self.open_path(
            os.path.expanduser("~/Documents")
        )

        return "Opening Documents."

    # ----------------------------------------------------
    # Games
    # ----------------------------------------------------

    if "games" in cleaned or "open games" in cleaned:
        return (
            "The WOLF Games module is not installed yet. "
            "We can build it next."
        )

    # ----------------------------------------------------
    # Shutdown
    # ----------------------------------------------------

    if (
        "shutdown wolf" in cleaned
        or "close wolf ai" in cleaned
        or "exit wolf ai" in cleaned
    ):
        self.root.after(
            1000,
            self.root.destroy
        )

        return "Closing WOLF AI."

    # ----------------------------------------------------
    # Default
    # ----------------------------------------------------

    return (
        f"I heard: {original}. "
        "I don't have a command for that yet."
    )

# --------------------------------------------------------
# Calculation extraction
# --------------------------------------------------------

def extract_calculation(self, text):

    if "calculate" in text:
        expression = text.split(
            "calculate",
            1
        )[1].strip()

        return expression

    if "what is" in text:

        possible = text.split(
            "what is",
            1
        )[1].strip()

        if any(char.isdigit() for char in possible):
            return possible

    if re.fullmatch(
        r"[0-9+\-*/(). xX%^]+",
        text
    ):
        return text

    return None

# --------------------------------------------------------
# Note extraction
# --------------------------------------------------------

def extract_note_text(self, text):

    phrases = [
        "create note",
        "make a note",
        "write a note",
        "take a note"
    ]

    for phrase in phrases:

        if phrase in text:

            note = text.split(
                phrase,
                1
            )[1].strip()

            if note:
                return note

    return None

# --------------------------------------------------------
# Create note
# --------------------------------------------------------

def create_note(self, text):

    path = os.path.expanduser(
        "~/WolfOS/wolf_note.txt"
    )

    try:

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"\n[{timestamp}]\n{text}\n"
            )

        self.open_path(path)

        return "I added that to WOLF Notes."

    except Exception as error:

        return f"I could not create the note: {error}"

# --------------------------------------------------------
# Battery
# --------------------------------------------------------

def get_battery(self):

    try:

        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True
        )

        output = result.stdout

        match = re.search(
            r"(\d+)%.*?;(.*?)\n",
            output
        )

        if match:

            percentage = match.group(1)

            return f"Your battery is at {percentage} percent."

        match = re.search(
            r"(\d+)%",
            output
        )

        if match:

            return (
                f"Your battery is at "
                f"{match.group(1)} percent."
            )

        return "I could not determine the battery level."

    except Exception:

        return "I could not check the battery."

# --------------------------------------------------------
# Open application
# --------------------------------------------------------

def open_application(self, application):

    try:

        subprocess.Popen(
            ["open", "-a", application]
        )

    except Exception:
        pass

# --------------------------------------------------------
# Open file/folder
# --------------------------------------------------------

def open_path(self, path):

    try:

        subprocess.Popen(
            ["open", path]
        )

    except Exception:
        pass

# --------------------------------------------------------
# Launch WOLF OS
# --------------------------------------------------------

def launch_wolf_os(self):

    launcher = os.path.expanduser(
        "~/WolfOS/wolf_launcher.py"
    )

    try:

        subprocess.Popen(
            [
                "/usr/local/bin/python3.14",
                launcher
            ]
        )

    except Exception:
        try:

            subprocess.Popen(
                [
                    "python3.14",
                    launcher
                ]
            )

        except Exception:
            pass

# --------------------------------------------------------
# Text to speech
# --------------------------------------------------------

def speak(self, text):

    def speak_thread():

        try:

            subprocess.Popen(
                ["say", text]
            )

        except Exception:
            pass

    threading.Thread(
        target=speak_thread,
        daemon=True
    ).start()

# --------------------------------------------------------
# Wake word detection
# --------------------------------------------------------

def contains_wake_word(self, text):

    words = re.findall(
        r"[a-zA-Z]+",
        text.lower()
    )

    accepted = {
        "wolf",
        "wulf",
        "wol",
        "wolve",
        "wolfe",
        "woof",
        "woolf"
    }

    if any(word in accepted for word in words):
        return True

    # Fuzzy matching for small transcription mistakes
    for word in words:

        if self.levenshtein_distance(
            word,
            "wolf"
        ) <= 1:
            return True

    return False

# --------------------------------------------------------
# Levenshtein distance
# --------------------------------------------------------

def levenshtein_distance(self, a, b):

    if len(a) < len(b):
        return self.levenshtein_distance(b, a)

    previous = list(range(len(b) + 1))

    for i, char_a in enumerate(a, start=1):

        current = [i]

        for j, char_b in enumerate(b, start=1):

            insert = current[j - 1] + 1
            delete = previous[j] + 1
            replace = previous[j - 1]

            if char_a != char_b:
                replace += 1

            current.append(
                min(insert, delete, replace)
            )

        previous = current

    return previous[-1]

# --------------------------------------------------------
# Remove wake word
# --------------------------------------------------------

def remove_wake_word(self, text):

    words = text.split()

    accepted = {
        "wolf",
        "wulf",
        "wol",
        "wolve",
        "wolfe",
        "woof",
        "woolf"
    }

    for index, word in enumerate(words):

        clean = re.sub(
            r"[^a-zA-Z]",
            "",
            word.lower()
        )

        if (
            clean in accepted
            or self.levenshtein_distance(
                clean,
                "wolf"
            ) <= 1
        ):

            words.pop(index)
            break

    return " ".join(words).strip(
        " ,.!?"
    )

# --------------------------------------------------------
# Voice mode
# --------------------------------------------------------

def toggle_voice_mode(self):

    if self.voice_mode:

        self.voice_mode = False

        self.voice_button.config(
            text="🎤 WAKE WOLF"
        )

        self.status_label.config(
            text="● ONLINE",
            fg="#39ff88"
        )

        self.add_message(
            "WOLF",
            "Voice mode stopped."
        )

    else:

        self.voice_mode = True

        self.voice_button.config(
            text="🛑 STOP LISTENING"
        )

        self.status_label.config(
            text="● LISTENING",
            fg="#ffd43b"
        )

        self.add_message(
            "WOLF",
            "Wake-word mode active. Say \"WOLF\" followed by a command."
        )

        self.listening_thread = threading.Thread(
            target=self.continuous_listen,
            daemon=True
        )

        self.listening_thread.start()

# --------------------------------------------------------
# Continuous microphone listening
# --------------------------------------------------------

def continuous_listen(self):

    if self.model is None:

        self.root.after(
            0,
            lambda: self.add_message(
                "WOLF",
                "Loading voice recognition model..."
            )
        )

        try:

            self.model = whisper.load_model(
                "base"
            )

        except Exception as error:

            self.voice_mode = False

            self.root.after(
                0,
                lambda: self.add_message(
                    "WOLF",
                    f"Voice model error: {error}"
                )
            )

            return

    while self.voice_mode:

        try:

            recording = sd.rec(
                int(
                    LISTEN_SECONDS *
                    SAMPLE_RATE
                ),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="int16"
            )

            sd.wait()

            audio = (
                recording
                .flatten()
                .astype(np.float32)
                / 32768.0
            )

            result = self.model.transcribe(
                audio,
                language="en",
                fp16=False
            )

            text = result.get(
                "text",
                ""
            ).strip()

            if not text:
                continue

            print(
                f"WOLF HEARD: {text}"
            )

            if self.contains_wake_word(text):

                command = self.remove_wake_word(
                    text
                )

                if command:

                    self.root.after(
                        0,
                        lambda c=command: self.process_voice_command(c)
                    )

                    time.sleep(1)

        except Exception as error:

            print(
                f"Voice error: {error}"
            )

            time.sleep(1)

# --------------------------------------------------------
# Process voice command
# --------------------------------------------------------

def process_voice_command(self, command):

    self.add_message(
        "YOU 🎤",
        command
    )

    response = self.get_response(
        command
    )

    self.add_message(
        "WOLF",
        response
    )

    self.speak(response)
```

# ============================================================

# Start WOLF AI

# ============================================================

root = tk.Tk()

app = WolfAI(root)

root.mainloop()


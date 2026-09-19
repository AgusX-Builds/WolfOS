import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import re
import ast
import operator
import threading
import time

try:
    import sounddevice as sd
    import whisper
    import numpy as np
    VOICE_AVAILABLE = True
except Exception:
    VOICE_AVAILABLE = False


class SafeCalculator(ast.NodeVisitor):

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid number")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        operation = self.OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Invalid operator")

        return operation(left, right)

    def visit_UnaryOp(self, node):
        value = self.visit(node.operand)

        operation = self.OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Invalid operator")

        return operation(value)

    def generic_visit(self, node):
        raise ValueError("Invalid calculation")


class WolfAI:

    def __init__(self, root):

        self.root = root

        self.root.title("WOLF AI")
        self.root.geometry("900x700")
        self.root.configure(bg="#07111F")

        self.listening = False
        self.listening_thread = None

        self.build_interface()

        self.add_message(
            "WOLF",
            "Hello. I am WOLF AI."
        )

        self.add_message(
            "WOLF",
            "Say 'WOLF' followed by a command."
        )

        if VOICE_AVAILABLE:
            self.add_message(
                "SYSTEM",
                "Voice system ready."
            )
        else:
            self.add_message(
                "SYSTEM",
                "Voice system unavailable."
            )

    # ---------------------------------------------------------
    # INTERFACE
    # ---------------------------------------------------------

    def build_interface(self):

        header = tk.Frame(
            self.root,
            bg="#07111F"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        title = tk.Label(
            header,
            text="🐺 WOLF AI",
            font=("Arial", 28, "bold"),
            fg="#FFFFFF",
            bg="#07111F"
        )

        title.pack(side="left")

        self.status_label = tk.Label(
            header,
            text="● ONLINE",
            font=("Arial", 12, "bold"),
            fg="#4CFF88",
            bg="#07111F"
        )

        self.status_label.pack(
            side="right",
            padx=10
        )

        subtitle = tk.Label(
            self.root,
            text="MAIN AI • VOICE • COMMAND CENTER",
            font=("Arial", 11),
            fg="#8FA6BF",
            bg="#07111F"
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 13),
            bg="#0D1B2A",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat",
            borderwidth=0
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.chat.configure(
            state="disabled"
        )

        bottom = tk.Frame(
            self.root,
            bg="#07111F"
        )

        bottom.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.entry = tk.Entry(
            bottom,
            font=("Arial", 14),
            bg="#10243A",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
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
            command=self.send_text,
            font=("Arial", 11, "bold"),
            bg="#1B5E8A",
            fg="white",
            activebackground="#287FB5",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10
        )

        send_button.pack(
            side="left",
            padx=5
        )

        voice_button = tk.Button(
            bottom,
            text="🎤 WAKE WOLF",
            command=self.toggle_voice_mode,
            font=("Arial", 11, "bold"),
            bg="#183A55",
            fg="white",
            activebackground="#245777",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=10
        )

        voice_button.pack(
            side="left",
            padx=5
        )

    # ---------------------------------------------------------
    # CHAT
    # ---------------------------------------------------------

    def add_message(self, sender, message):

        self.chat.configure(
            state="normal"
        )

        self.chat.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )

        self.chat.see(
            tk.END
        )

        self.chat.configure(
            state="disabled"
        )

    def send_text(self):

        command = self.entry.get().strip()

        if not command:
            return

        self.entry.delete(
            0,
            tk.END
        )

        self.add_message(
            "YOU",
            command
        )

        response = self.handle_command(
            command
        )

        self.add_message(
            "WOLF",
            response
        )

        self.speak(
            response
        )

    # ---------------------------------------------------------
    # AI ACTIVATION
    # ---------------------------------------------------------

    def activate_ai(self, ai_name):

        ai_programs = {

            "nova": "nova_ai.py",

            "volt": "volt_ai.py",

            "aegis": "aegis_ai.py",

            "pixel": "pixel_ai.py",

            "forge": "forge_ai.py",

            "nexus": "nexus_ai.py",

            "orion": "orion_ai.py",

            "echo": "echo_ai.py"
        }

        ai_name = ai_name.lower().strip()

        if ai_name not in ai_programs:

            return f"I don't know an AI named {ai_name.upper()}."

        filename = ai_programs[ai_name]

        program_path = os.path.expanduser(
            f"~/WolfOS/{filename}"
        )

        if not os.path.exists(program_path):

            return (
                f"{ai_name.upper()} is not installed yet. "
                f"I could not find {filename}."
            )

        try:

            subprocess.Popen(
                [
                    "/usr/local/bin/python3.14",
                    program_path
                ]
            )

            return f"Activating {ai_name.upper()}."

        except Exception as error:

            return (
                f"I could not activate {ai_name.upper()}: "
                f"{error}"
            )

    def check_ai_activation(self, command):

        command_lower = command.lower().strip()

        ai_names = [
            "nova",
            "volt",
            "aegis",
            "pixel",
            "forge",
            "nexus",
            "orion",
            "echo"
        ]

        activation_words = [
            "activate",
            "open",
            "start",
            "launch"
        ]

        for ai_name in ai_names:

            if ai_name not in command_lower:
                continue

            for word in activation_words:

                if word in command_lower:

                    return self.activate_ai(
                        ai_name
                    )

        return None

    # ---------------------------------------------------------
    # COMMAND HANDLER
    # ---------------------------------------------------------

    def handle_command(self, command):

        command_lower = command.lower().strip()

        # FIRST: check for AI activation
        ai_response = self.check_ai_activation(
            command_lower
        )

        if ai_response is not None:

            return ai_response

        # -----------------------------------------------------
        # IDENTITY
        # -----------------------------------------------------

        if (
            "who are you" in command_lower
            or "what are you" in command_lower
        ):

            return (
                "I am WOLF AI, the main AI of WOLF OS."
            )

        # -----------------------------------------------------
        # GREETINGS
        # -----------------------------------------------------

        if command_lower in [
            "hello",
            "hi",
            "hey",
            "hello wolf",
            "hi wolf"
        ]:

            return (
                "Hello. WOLF systems are online."
            )

        # -----------------------------------------------------
        # HELP
        # -----------------------------------------------------

        if (
            "help" in command_lower
            or "what can you do" in command_lower
        ):

            return (
                "I can control WOLF OS, open applications, "
                "create notes, calculate numbers, check the "
                "battery, and activate other WOLF AI systems."
            )

        # -----------------------------------------------------
        # TIME
        # -----------------------------------------------------

        if "time" in command_lower:

            return time.strftime(
                "The current time is %I:%M %p."
            )

        # -----------------------------------------------------
        # DATE
        # -----------------------------------------------------

        if (
            "date" in command_lower
            or "day is it" in command_lower
        ):

            return time.strftime(
                "Today is %A, %B %d, %Y."
            )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        if "status" in command_lower:

            return (
                "WOLF OS is online. "
                "Main systems operational."
            )

        # -----------------------------------------------------
        # OPEN SAFARI
        # -----------------------------------------------------

        if (
            "open safari" in command_lower
            or "launch safari" in command_lower
        ):

            subprocess.Popen(
                ["open", "-a", "Safari"]
            )

            return "Opening Safari."

        # -----------------------------------------------------
        # OPEN TERMINAL
        # -----------------------------------------------------

        if (
            "open terminal" in command_lower
            or "launch terminal" in command_lower
        ):

            subprocess.Popen(
                ["open", "-a", "Terminal"]
            )

            return "Opening Terminal."

        # -----------------------------------------------------
        # OPEN FINDER
        # -----------------------------------------------------

        if (
            "open finder" in command_lower
            or "launch finder" in command_lower
        ):

            subprocess.Popen(
                ["open", "-a", "Finder"]
            )

            return "Opening Finder."

        # -----------------------------------------------------
        # OPEN MUSIC
        # -----------------------------------------------------

        if (
            "open music" in command_lower
            or "launch music" in command_lower
        ):

            subprocess.Popen(
                ["open", "-a", "Music"]
            )

            return "Opening Music."

        # -----------------------------------------------------
        # OPEN CALCULATOR
        # -----------------------------------------------------

        if (
            "open calculator" in command_lower
            or "launch calculator" in command_lower
        ):

            subprocess.Popen(
                ["open", "-a", "Calculator"]
            )

            return "Opening Calculator."

        # -----------------------------------------------------
        # OPEN SETTINGS
        # -----------------------------------------------------

        if (
            "open settings" in command_lower
            or "system settings" in command_lower
        ):

            subprocess.Popen(
                ["open", "x-apple.systempreferences:"]
            )

            return "Opening System Settings."

        # -----------------------------------------------------
        # OPEN DOWNLOADS
        # -----------------------------------------------------

        if "open downloads" in command_lower:

            subprocess.Popen(
                ["open", os.path.expanduser("~/Downloads")]
            )

            return "Opening Downloads."

        # -----------------------------------------------------
        # OPEN DESKTOP
        # -----------------------------------------------------

        if "open desktop" in command_lower:

            subprocess.Popen(
                ["open", os.path.expanduser("~/Desktop")]
            )

            return "Opening Desktop."

        # -----------------------------------------------------
        # OPEN DOCUMENTS
        # -----------------------------------------------------

        if "open documents" in command_lower:

            subprocess.Popen(
                ["open", os.path.expanduser("~/Documents")]
            )

            return "Opening Documents."

        # -----------------------------------------------------
        # OPEN WOLF FOLDER
        # -----------------------------------------------------

        if (
            "open wolf folder" in command_lower
            or "open wolf os folder" in command_lower
        ):

            subprocess.Popen(
                ["open", os.path.expanduser("~/WolfOS")]
            )

            return "Opening the WOLF OS folder."

        # -----------------------------------------------------
        # OPEN NOTES
        # -----------------------------------------------------

        if (
            "open notes" in command_lower
            or "launch notes" in command_lower
        ):

            notes_path = os.path.expanduser(
                "~/WolfOS/wolf_note.txt"
            )

            if not os.path.exists(notes_path):

                open(notes_path, "w").close()

            subprocess.Popen(
                ["open", notes_path]
            )

            return "Opening WOLF notes."

        # -----------------------------------------------------
        # CREATE NOTE
        # -----------------------------------------------------

        if (
            "create note" in command_lower
            or "make a note" in command_lower
            or "write a note" in command_lower
        ):

            note = command

            for phrase in [
                "create note",
                "make a note",
                "write a note"
            ]:

                note = re.sub(
                    phrase,
                    "",
                    note,
                    flags=re.IGNORECASE
                )

            note = note.strip()

            if not note:

                return "What would you like me to write?"

            notes_path = os.path.expanduser(
                "~/WolfOS/wolf_note.txt"
            )

            with open(
                notes_path,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    note + "\n"
                )

            return "Note saved."

        # -----------------------------------------------------
        # BATTERY
        # -----------------------------------------------------

        if "battery" in command_lower:

            try:

                result = subprocess.check_output(
                    ["pmset", "-g", "batt"],
                    text=True
                )

                match = re.search(
                    r"(\d+)%"
                    ,
                    result
                )

                if match:

                    return (
                        f"The battery is at "
                        f"{match.group(1)} percent."
                    )

                return "I could not read the battery level."

            except Exception:

                return "I could not check the battery."

        # -----------------------------------------------------
        # CALCULATOR
        # -----------------------------------------------------

        if (
            command_lower.startswith("calculate ")
            or command_lower.startswith("what is ")
            or command_lower.startswith("compute ")
        ):

            expression = command

            expression = re.sub(
                r"^(calculate|what is|compute)\s+",
                "",
                expression,
                flags=re.IGNORECASE
            )

            expression = expression.replace(
                "x",
                "*"
            )

            try:

                tree = ast.parse(
                    expression,
                    mode="eval"
                )

                calculator = SafeCalculator()

                result = calculator.visit(
                    tree.body
                )

                return f"The answer is {result}."

            except Exception:

                return "I could not calculate that safely."

        # -----------------------------------------------------
        # GAMES
        # -----------------------------------------------------

        if (
            "game" in command_lower
            or "games" in command_lower
        ):

            return (
                "The WOLF gaming system is ready for future games."
            )

        # -----------------------------------------------------
        # GOODBYE
        # -----------------------------------------------------

        if (
            "goodbye" in command_lower
            or command_lower == "bye"
        ):

            return "Goodbye."

        # -----------------------------------------------------
        # DEFAULT
        # -----------------------------------------------------

        return (
            "I understand the command, but I do not have "
            "a dedicated action for it yet."
        )

    # ---------------------------------------------------------
    # VOICE
    # ---------------------------------------------------------

    def toggle_voice_mode(self):

        if not VOICE_AVAILABLE:

            self.add_message(
                "SYSTEM",
                "Voice libraries are not available."
            )

            return

        if self.listening:

            self.listening = False

            self.status_label.config(
                text="● ONLINE",
                fg="#4CFF88"
            )

            self.add_message(
                "SYSTEM",
                "Wake-word mode stopped."
            )

            return

        self.listening = True

        self.status_label.config(
            text="● LISTENING",
            fg="#FFD84C"
        )

        self.add_message(
            "SYSTEM",
            "Wake-word mode active. Say 'WOLF' followed by a command."
        )

        self.listening_thread = threading.Thread(
            target=self.continuous_listen,
            daemon=True
        )

        self.listening_thread.start()

    def continuous_listen(self):

        try:

            model = whisper.load_model(
                "base"
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.add_message(
                    "SYSTEM",
                    f"Could not load Whisper: {error}"
                )
            )

            self.listening = False

            return

        sample_rate = 16000

        while self.listening:

            try:

                recording = sd.rec(
                    int(sample_rate * 4),
                    samplerate=sample_rate,
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

                result = model.transcribe(
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

                cleaned = text.lower().strip()

                if self.contains_wake_word(cleaned):

                    command = self.remove_wake_word(
                        text
                    )

                    if command.strip():

                        self.root.after(
                            0,
                            lambda c=command:
                            self.process_voice_command(c)
                        )

            except Exception as error:

                self.root.after(
                    0,
                    lambda e=error:
                    self.add_message(
                        "VOICE ERROR",
                        str(e)
                    )
                )

                time.sleep(1)

    # ---------------------------------------------------------
    # WAKE WORD
    # ---------------------------------------------------------

    def contains_wake_word(self, text):

        words = re.findall(
            r"[a-zA-Z]+",
            text.lower()
        )

        wake_words = [
            "wolf",
            "wulf",
            "wol",
            "wolve",
            "wolfe",
            "woof",
            "woolf"
        ]

        for word in words:

            if word in wake_words:

                return True

            if self.levenshtein(
                word,
                "wolf"
            ) <= 1:

                return True

        return False

    def remove_wake_word(self, text):

        pattern = (
            r"\b("
            r"wolf|wulf|wol|wolve|wolfe|"
            r"woof|woolf"
            r")\b"
        )

        command = re.sub(
            pattern,
            "",
            text,
            count=1,
            flags=re.IGNORECASE
        )

        return command.strip(
            " ,.!?"
        )

    def levenshtein(self, a, b):

        if len(a) < len(b):

            return self.levenshtein(
                b,
                a
            )

        if len(b) == 0:

            return len(a)

        previous = list(
            range(len(b) + 1)
        )

        for i, char_a in enumerate(a, 1):

            current = [
                i
            ]

            for j, char_b in enumerate(b, 1):

                insertions = (
                    previous[j] + 1
                )

                deletions = (
                    current[j - 1] + 1
                )

                substitutions = (
                    previous[j - 1]
                    + (
                        char_a != char_b
                    )
                )

                current.append(
                    min(
                        insertions,
                        deletions,
                        substitutions
                    )
                )

            previous = current

        return previous[-1]

    # ---------------------------------------------------------
    # VOICE COMMAND PROCESSING
    # ---------------------------------------------------------

    def process_voice_command(self, command):

        self.add_message(
            "YOU 🎤",
            command
        )

        response = self.handle_command(
            command
        )

        self.add_message(
            "WOLF",
            response
        )

        self.speak(
            response
        )

    # ---------------------------------------------------------
    # SPEECH
    # ---------------------------------------------------------

    def speak(self, text):

        def speak_thread():

            try:

                subprocess.run(
                    [
                        "say",
                        text
                    ],
                    check=False
                )

            except Exception:

                pass

        threading.Thread(
            target=speak_thread,
            daemon=True
        ).start()


# -------------------------------------------------------------
# START WOLF
# -------------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = WolfAI(
        root
    )

    root.mainloop()

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import random
import subprocess
import os
import threading
import time
import sounddevice as sd
import whisper
import numpy as np
import ast
import operator


# ============================================================
# WOLF OS PATHS
# ============================================================

WOLF_FOLDER = os.path.expanduser("~/WolfOS")
NOTES_FILE = os.path.join(WOLF_FOLDER, "wolf_note.txt")

SAMPLE_RATE = 16000
LISTEN_SECONDS = 3


# ============================================================
# SAFE CALCULATOR
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def safe_calculate(expression):
    """
    Safely calculate basic mathematical expressions.
    """

    expression = expression.replace("x", "*")
    expression = expression.replace("X", "*")
    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("times", "*")
    expression = expression.replace("divided by", "/")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate_node(tree.body)
    except Exception:
        return None


def evaluate_node(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError()

    if isinstance(node, ast.BinOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError()

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError()

        return operation(evaluate_node(node.operand))

    raise ValueError()


# ============================================================
# WOLF AI
# ============================================================

class WolfAI:

    def __init__(self, root):

        self.root = root

        self.voice_mode = False
        self.model = None

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title("WOLF AI")
        self.root.geometry("900x650")
        self.root.configure(bg="#07111F")

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.root,
            bg="#07111F"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        title = tk.Label(
            header,
            text="🐺 WOLF AI",
            font=("Arial", 26, "bold"),
            bg="#07111F",
            fg="white"
        )

        title.pack(side="left")

        self.status = tk.Label(
            header,
            text="● ONLINE",
            font=("Arial", 12, "bold"),
            bg="#07111F",
            fg="#55FF88"
        )

        self.status.pack(side="right")


        # ----------------------------------------------------
        # CHAT
        # ----------------------------------------------------

        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 13),
            bg="#0D1B2A",
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
            pady=10
        )

        self.chat.config(state="disabled")


        # ----------------------------------------------------
        # INPUT AREA
        # ----------------------------------------------------

        input_frame = tk.Frame(
            self.root,
            bg="#07111F"
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )


        self.entry = tk.Entry(
            input_frame,
            font=("Arial", 14),
            bg="#14283D",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12
        )

        self.entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )


        send_button = tk.Button(
            input_frame,
            text="SEND",
            font=("Arial", 11, "bold"),
            bg="#244A68",
            fg="white",
            activebackground="#356B94",
            activeforeground="white",
            relief="flat",
            command=self.send_message
        )

        send_button.pack(
            side="left",
            padx=(10, 0),
            ipadx=15,
            ipady=8
        )


        # ----------------------------------------------------
        # VOICE BUTTON
        # ----------------------------------------------------

        self.voice_button = tk.Button(
            input_frame,
            text="🎤 WAKE WOLF",
            font=("Arial", 11, "bold"),
            bg="#244A68",
            fg="white",
            activebackground="#356B94",
            activeforeground="white",
            relief="flat",
            command=self.toggle_voice_mode
        )

        self.voice_button.pack(
            side="left",
            padx=(10, 0),
            ipadx=10,
            ipady=8
        )


        # ----------------------------------------------------
        # STARTUP
        # ----------------------------------------------------

        self.add_message(
            "WOLF",
            "🐺 WOLF AI initialized."
        )

        self.add_message(
            "WOLF",
            "Advanced command system loading..."
        )

        self.add_message(
            "WOLF",
            "Voice system loading..."
        )

        threading.Thread(
            target=self.load_whisper,
            daemon=True
        ).start()


    # ========================================================
    # WHISPER
    # ========================================================

    def load_whisper(self):

        try:

            self.model = whisper.load_model("base")

            self.root.after(
                0,
                lambda: self.add_message(
                    "WOLF",
                    '🎤 Voice AI ready. Press "WAKE WOLF" to activate.'
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.add_message(
                    "WOLF",
                    f"Voice system error: {error}"
                )
            )


    # ========================================================
    # CHAT
    # ========================================================

    def add_message(self, sender, message):

        self.chat.config(state="normal")

        self.chat.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )

        self.chat.see(tk.END)

        self.chat.config(state="disabled")


    # ========================================================
    # TYPED MESSAGE
    # ========================================================

    def send_message(self):

        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(0, tk.END)

        self.add_message(
            "YOU",
            text
        )

        response = self.get_response(text.lower())

        self.add_message(
            "WOLF",
            response
        )

        self.speak(response)


    # ========================================================
    # VOICE MODE
    # ========================================================

    def toggle_voice_mode(self):

        if self.model is None:

            self.add_message(
                "WOLF",
                "🎤 Voice AI is still loading."
            )

            return


        self.voice_mode = not self.voice_mode


        if self.voice_mode:

            self.voice_button.config(
                text="🔴 STOP WOLF",
                bg="#7A2525"
            )

            self.status.config(
                text="● LISTENING",
                fg="#FF5555"
            )

            self.add_message(
                "WOLF",
                "🎤 Continuous listening activated."
            )

            self.add_message(
                "WOLF",
                'Say "WOLF" followed by a command.'
            )

            threading.Thread(
                target=self.continuous_listen,
                daemon=True
            ).start()


        else:

            self.voice_button.config(
                text="🎤 WAKE WOLF",
                bg="#244A68"
            )

            self.status.config(
                text="● ONLINE",
                fg="#55FF88"
            )

            self.add_message(
                "WOLF",
                "🎤 Continuous listening stopped."
            )


    # ========================================================
    # CONTINUOUS LISTENING
    # ========================================================

    def continuous_listen(self):

        while self.voice_mode:

            try:

                recording = sd.rec(
                    int(LISTEN_SECONDS * SAMPLE_RATE),
                    samplerate=SAMPLE_RATE,
                    channels=1,
                    dtype="int16"
                )

                sd.wait()


                if not self.voice_mode:
                    break


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


                text = result["text"].strip()


                if not text:
                    continue


                lower_text = text.lower().strip()


                # ------------------------------------------------
                # ONLY RESPOND WHEN "WOLF" IS HEARD
                # ------------------------------------------------

                if not self.contains_wake_word(lower_text):
                    continue


                self.root.after(
                    0,
                    lambda t=text: self.handle_wake_command(t)
                )


                time.sleep(2)


            except Exception as error:

                self.root.after(
                    0,
                    lambda e=str(error): self.add_message(
                        "WOLF",
                        f"Microphone error: {e}"
                    )
                )

                time.sleep(2)


    # ========================================================
    # WAKE WORD CHECK
    # ========================================================

    def contains_wake_word(self, text):

        words = text.split()

        for word in words:

            cleaned = word.strip(
                ".,!?;:'\""
            )

            if cleaned == "wolf":
                return True

        return False


    # ========================================================
    # HANDLE VOICE COMMAND
    # ========================================================

    def handle_wake_command(self, text):

        self.add_message(
            "YOU",
            f"🎤 {text}"
        )


        clean_text = text.lower().strip()


        words = clean_text.split()


        # Remove WOLF wake word

        if "wolf" in words:

            index = words.index("wolf")

            words.pop(index)


        clean_text = " ".join(words)

        clean_text = clean_text.lstrip(
            " ,.!?"
        )


        if not clean_text:

            response = "🐺 WOLF is listening."

        else:

            response = self.get_response(
                clean_text
            )


        self.add_message(
            "WOLF",
            response
        )

        self.speak(response)


    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    def speak(self, text):

        def speak_thread():

            try:

                subprocess.Popen(
                    [
                        "say",
                        text
                    ]
                )

            except Exception:
                pass


        threading.Thread(
            target=speak_thread,
            daemon=True
        ).start()


    # ========================================================
    # MAIN BRAIN
    # ========================================================

    def get_response(self, text):

        text = text.lower().strip()


        # ----------------------------------------------------
        # HELLO
        # ----------------------------------------------------

        if any(word in text for word in [
            "hello",
            "hi",
            "hey"
        ]):

            responses = [
                "Hello. WOLF is online.",
                "Hello. How can I help?",
                "WOLF systems ready."
            ]

            return random.choice(responses)


        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        if "help" in text:

            return (
                "🐺 WOLF commands:\n"
                "• What time is it?\n"
                "• What is today's date?\n"
                "• What is my battery?\n"
                "• Open Safari\n"
                "• Open Terminal\n"
                "• Open Downloads\n"
                "• Open Desktop\n"
                "• Open Music\n"
                "• Open Notes\n"
                "• Open WOLF folder\n"
                "• Open WOLF OS\n"
                "• Take a note: your text\n"
                "• Calculate 25 times 8\n"
                "• What is your status?"
            )


        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        if (
            "what time" in text
            or "current time" in text
            or text == "time"
            or "tell me the time" in text
        ):

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            return f"The current time is {current_time}."


        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if (
            "what date" in text
            or "today's date" in text
            or "todays date" in text
            or text == "date"
            or "what day is it" in text
        ):

            current_date = datetime.now().strftime(
                "%A, %B %d, %Y"
            )

            return f"Today is {current_date}."


        # ----------------------------------------------------
        # BATTERY
        # ----------------------------------------------------

        if (
            "battery" in text
            or "charge" in text
            or "power level" in text
        ):

            return self.get_battery()


        # ----------------------------------------------------
        # CALCULATOR
        # ----------------------------------------------------

        if (
            "calculate" in text
            or "what is" in text
            or "how much is" in text
        ):

            result = self.calculate_command(text)

            if result is not None:

                return f"The answer is {result}."


        # ----------------------------------------------------
        # TAKE A NOTE
        # ----------------------------------------------------

        if (
            "take a note" in text
            or "write a note" in text
            or "make a note" in text
            or text.startswith("note ")
        ):

            return self.create_note(text)


        # ----------------------------------------------------
        # OPEN SAFARI
        # ----------------------------------------------------

        if (
            "open safari" in text
            or "start safari" in text
        ):

            self.open_app("Safari")

            return "Safari is opening."


        # ----------------------------------------------------
        # OPEN TERMINAL
        # ----------------------------------------------------

        if (
            "open terminal" in text
            or "start terminal" in text
        ):

            self.open_app("Terminal")

            return "Terminal is opening."


        # ----------------------------------------------------
        # OPEN MUSIC
        # ----------------------------------------------------

        if (
            "open music" in text
            or "start music" in text
        ):

            self.open_app("Music")

            return "Music is opening."


        # ----------------------------------------------------
        # OPEN FINDER
        # ----------------------------------------------------

        if (
            "open finder" in text
            or "start finder" in text
        ):

            self.open_app("Finder")

            return "Finder is opening."


        # ----------------------------------------------------
        # OPEN DOWNLOADS
        # ----------------------------------------------------

        if (
            "open downloads" in text
            or "show downloads" in text
        ):

            self.open_folder(
                os.path.expanduser("~/Downloads")
            )

            return "Opening Downloads."


        # ----------------------------------------------------
        # OPEN DESKTOP
        # ----------------------------------------------------

        if (
            "open desktop" in text
            or "show desktop" in text
        ):

            self.open_folder(
                os.path.expanduser("~/Desktop")
            )

            return "Opening Desktop."


        # ----------------------------------------------------
        # OPEN DOCUMENTS
        # ----------------------------------------------------

        if (
            "open documents" in text
            or "show documents" in text
        ):

            self.open_folder(
                os.path.expanduser("~/Documents")
            )

            return "Opening Documents."


        # ----------------------------------------------------
        # OPEN NOTES
        # ----------------------------------------------------

        if (
            "open notes" in text
            or "show notes" in text
        ):

            return self.open_notes()


        # ----------------------------------------------------
        # OPEN WOLF FOLDER
        # ----------------------------------------------------

        if (
            "open wolf folder" in text
            or "show wolf folder" in text
            or "open wolf files" in text
        ):

            self.open_folder(
                WOLF_FOLDER
            )

            return "Opening the WOLF OS folder."


        # ----------------------------------------------------
        # OPEN WOLF OS
        # ----------------------------------------------------

        if (
            "open wolf os" in text
            or "start wolf os" in text
            or "launch wolf os" in text
        ):

            return self.launch_wolf_os()


        # ----------------------------------------------------
        # GAMES
        # ----------------------------------------------------

        if (
            "games" in text
            or "game" in text
        ):

            return (
                "WOLF Games is not installed yet. "
                "That module is coming soon."
            )


        # ----------------------------------------------------
        # WHO ARE YOU
        # ----------------------------------------------------

        if (
            "who are you" in text
            or "what are you" in text
        ):

            return (
                "I am WOLF AI, the main artificial "
                "intelligence of WOLF OS."
            )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if (
            "status" in text
            or "system status" in text
            or "how are you" in text
        ):

            return (
                "🐺 WOLF systems are online. "
                "Voice recognition is operational."
            )


        # ----------------------------------------------------
        # WOLF
        # ----------------------------------------------------

        if text == "wolf":

            return (
                "🐺 Yes? WOLF is listening."
            )


        # ----------------------------------------------------
        # SHUTDOWN WARNING
        # ----------------------------------------------------

        if (
            "shutdown" in text
            or "turn off computer" in text
            or "shut down computer" in text
        ):

            return (
                "I won't shut down the computer "
                "automatically yet."
            )


        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        return (
            "I heard you, but I don't have a command "
            f"for '{text}' yet."
        )


    # ========================================================
    # BATTERY
    # ========================================================

    def get_battery(self):

        try:

            result = subprocess.run(
                [
                    "pmset",
                    "-g",
                    "batt"
                ],
                capture_output=True,
                text=True
            )

            output = result.stdout


            # Find percentage

            import re

            match = re.search(
                r"(\d+)%",
                output
            )


            if match:

                percentage = match.group(1)

                if "AC Power" in output:

                    return (
                        f"Battery is at {percentage} percent "
                        "and the Mac is connected to power."
                    )

                return (
                    f"Battery is at {percentage} percent."
                )


            return "I couldn't read the battery level."

        except Exception:

            return "I couldn't access the battery information."


    # ========================================================
    # CALCULATE COMMAND
    # ========================================================

    def calculate_command(self, text):

        expression = text.lower()


        replacements = [
            ("calculate", ""),
            ("what is", ""),
            ("how much is", ""),
            ("please", ""),
            ("the answer to", ""),
        ]


        for phrase, replacement in replacements:

            expression = expression.replace(
                phrase,
                replacement
            )


        expression = expression.strip()

        expression = expression.replace(
            " divided by ",
            "/"
        )

        expression = expression.replace(
            " times ",
            "*"
        )

        expression = expression.replace(
            " plus ",
            "+"
        )

        expression = expression.replace(
            " minus ",
            "-"
        )


        # Only attempt if it looks mathematical

        allowed = set(
            "0123456789+-*/(). %"
        )


        if not any(
            char.isdigit()
            for char in expression
        ):

            return None


        if not all(
            char in allowed
            for char in expression
        ):

            return None


        result = safe_calculate(
            expression
        )


        return result


    # ========================================================
    # CREATE NOTE
    # ========================================================

    def create_note(self, text):

        note = text


        prefixes = [
            "take a note:",
            "take a note",
            "write a note:",
            "write a note",
            "make a note:",
            "make a note",
            "note:"
        ]


        for prefix in prefixes:

            if note.startswith(prefix):

                note = note[
                    len(prefix):
                ].strip()

                break


        if not note:

            return "What would you like me to write?"


        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )


        try:

            with open(
                NOTES_FILE,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    f"\n[{timestamp}] {note}\n"
                )


            return (
                "📝 Note saved successfully."
            )


        except Exception as error:

            return (
                f"I couldn't save the note: {error}"
            )


    # ========================================================
    # OPEN APP
    # ========================================================

    def open_app(self, app_name):

        try:

            subprocess.Popen(
                [
                    "open",
                    "-a",
                    app_name
                ]
            )

        except Exception:
            pass


    # ========================================================
    # OPEN FOLDER
    # ========================================================

    def open_folder(self, path):

        try:

            subprocess.Popen(
                [
                    "open",
                    path
                ]
            )

        except Exception:
            pass


    # ========================================================
    # OPEN NOTES
    # ========================================================

    def open_notes(self):

        try:

            if not os.path.exists(
                NOTES_FILE
            ):

                with open(
                    NOTES_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        "🐺 WOLF OS NOTES\n\n"
                    )


            subprocess.Popen(
                [
                    "open",
                    NOTES_FILE
                ]
            )


            return "Opening WOLF Notes."

        except Exception as error:

            return (
                f"I couldn't open Notes: {error}"
            )


    # ========================================================
    # LAUNCH WOLF OS
    # ========================================================

    def launch_wolf_os(self):

        launcher = os.path.join(
            WOLF_FOLDER,
            "wolf_launcher.py"
        )


        if not os.path.exists(
            launcher
        ):

            return (
                "I couldn't find the WOLF OS launcher."
            )


        try:

            subprocess.Popen(
                [
                    "/usr/local/bin/python3.14",
                    launcher
                ]
            )


            return "Launching the latest WOLF OS."

        except Exception as error:

            return (
                f"I couldn't launch WOLF OS: {error}"
            )


# ============================================================
# START WOLF AI
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WolfAI(root)

    root.mainloop()

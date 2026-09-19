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


# ============================================================
# WOLF OS
# ============================================================

WOLF_FOLDER = os.path.expanduser("~/WolfOS")
NOTES_FILE = os.path.join(WOLF_FOLDER, "wolf_note.txt")

SAMPLE_RATE = 16000

# Short chunks for continuous listening
LISTEN_SECONDS = 3


# ============================================================
# WOLF AI
# ============================================================

class WolfAI:

    def __init__(self, root):

        self.root = root

        self.root.title("WOLF AI")
        self.root.geometry("800x600")
        self.root.minsize(650, 450)
        self.root.configure(bg="#07111F")

        # Voice state
        self.voice_mode = False
        self.model = None

        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            root,
            bg="#0B1C30",
            height=70
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🐺 WOLF AI",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#0B1C30"
        )

        title.pack(
            side="left",
            padx=25
        )

        self.status = tk.Label(
            header,
            text="● ONLINE",
            font=("Helvetica", 11, "bold"),
            fg="#55FF88",
            bg="#0B1C30"
        )

        self.status.pack(
            side="right",
            padx=25
        )

        # ====================================================
        # CHAT
        # ====================================================

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Helvetica", 14),
            bg="#0A1727",
            fg="white",
            insertbackground="white",
            relief="flat",
            padx=15,
            pady=15
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(15, 10)
        )

        self.chat.config(state="disabled")

        # ====================================================
        # INPUT
        # ====================================================

        input_frame = tk.Frame(
            root,
            bg="#07111F"
        )

        input_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.entry = tk.Entry(
            input_frame,
            font=("Helvetica", 14),
            bg="#102238",
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
            self.send_message
        )

        send_button = tk.Button(
            input_frame,
            text="SEND",
            font=("Helvetica", 12, "bold"),
            bg="#163452",
            fg="white",
            activebackground="#214D75",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.send_message
        )

        send_button.pack(side="right")

        # ====================================================
        # VOICE BUTTON
        # ====================================================

        self.voice_button = tk.Button(
            input_frame,
            text="🎤 WAKE WOLF",
            font=("Helvetica", 12, "bold"),
            bg="#244A68",
            fg="white",
            activebackground="#326789",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.toggle_voice_mode
        )

        self.voice_button.pack(
            side="right",
            padx=(0, 10)
        )

        # ====================================================
        # START MESSAGE
        # ====================================================

        self.add_message(
            "WOLF",
            "Hello! 🐺 WOLF OS control system is online."
        )

        self.add_message(
            "WOLF",
            "I can now control parts of your WOLF OS."
        )

        self.add_message(
            "WOLF",
            "Type 'help' to see my commands."
        )

        self.add_message(
            "WOLF",
            "🎤 Voice AI is loading..."
        )

        self.entry.focus()

        # ====================================================
        # LOAD WHISPER
        # ====================================================

        threading.Thread(
            target=self.load_whisper,
            daemon=True
        ).start()


    # ========================================================
    # LOAD WHISPER
    # ========================================================

    def load_whisper(self):

        try:

            self.model = whisper.load_model("base")

            self.root.after(
                0,
                lambda: self.add_message(
                    "WOLF",
                    "🎤 Voice AI ready. Press WAKE WOLF to activate."
                )
            )

        except Exception as error:

            self.model = None

            self.root.after(
                0,
                lambda: self.add_message(
                    "WOLF",
                    f"Voice AI error: {error}"
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

        self.chat.config(state="disabled")

        self.chat.see(tk.END)


    # ========================================================
    # SEND
    # ========================================================

    def send_message(self, event=None):

        message = self.entry.get().strip()

        if not message:
            return

        self.entry.delete(
            0,
            tk.END
        )

        self.add_message(
            "YOU",
            message
        )

        response = self.get_response(message)

        self.add_message(
            "WOLF",
            response
        )

        self.speak(response)


    # ========================================================
    # TOGGLE WAKE MODE
    # ========================================================

    def toggle_voice_mode(self):

        if self.model is None:

            self.add_message(
                "WOLF",
                "🎤 Voice AI is still loading. Please wait."
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

                print("WOLF HEARD:", text)

                lower_text = text.lower().strip()

                # Only activate when WOLF is spoken
                if "wolf" not in lower_text:
                    continue

                self.root.after(
                    0,
                    lambda t=text: self.handle_wake_command(t)
                )

                # Give the command time to finish
                time.sleep(2)

            except Exception as error:

                self.root.after(
                    0,
                    lambda e=error: self.add_message(
                        "WOLF",
                        f"❌ Voice error: {e}"
                    )
                )

                time.sleep(1)


    # ========================================================
    # HANDLE WAKE COMMAND
    # ========================================================

    def handle_wake_command(self, text):

        self.add_message(
            "YOU",
            f"🎤 {text}"
        )

        clean_text = text.lower().strip()

        # Remove WOLF
        clean_text = clean_text.replace(
            "wolf",
            "",
            1
        ).strip()

        # Remove comma
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
    # SPEAK
    # ========================================================

    def speak(self, text):

        threading.Thread(
            target=lambda: subprocess.Popen(
                ["say", text]
            ),
            daemon=True
        ).start()


    # ========================================================
    # OPEN FILE
    # ========================================================

    def open_file(self, path):

        try:

            subprocess.Popen(
                ["open", path]
            )

            return True

        except Exception:

            return False


    # ========================================================
    # WOLF BRAIN
    # ========================================================

    def get_response(self, message):

        text = message.lower().strip()

        # ----------------------------------------------------
        # GREETINGS
        # ----------------------------------------------------

        if text in [
            "hi",
            "hello",
            "hey",
            "hola"
        ]:

            return random.choice([
                "Hello! 🐺",
                "Hey! WOLF is online.",
                "Hello, commander.",
                "Hey! What are we building today?"
            ])


        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        if text == "help":

            return (
                "WOLF COMMANDS\n\n"
                "🕒 time\n"
                "📅 date\n"
                "📊 status\n"
                "📝 open notes\n"
                "📁 open wolf folder\n"
                "🖥️ open wolf os\n"
                "🎮 open games\n"
                "❓ who are you\n"
                "🐺 wolf"
            )


        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        if "time" in text:

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            return (
                f"The current time is "
                f"{current_time}."
            )


        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if "date" in text or "day" in text:

            current_date = datetime.now().strftime(
                "%A, %B %d, %Y"
            )

            return (
                f"Today is "
                f"{current_date}."
            )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if "status" in text:

            return (
                "WOLF OS SYSTEM STATUS\n\n"
                "AI CORE: ONLINE 🟢\n"
                "SYSTEM: ONLINE 🟢\n"
                "SECURITY: ACTIVE 🟢\n"
                "COMMAND SYSTEM: ONLINE 🟢"
            )


        # ----------------------------------------------------
        # OPEN NOTES
        # ----------------------------------------------------

        if (
            "open notes" in text
            or "open note" in text
            or text == "notes"
        ):

            if self.open_file(NOTES_FILE):

                return (
                    "Opening WOLF Notes. 📝"
                )

            return (
                "I couldn't open WOLF Notes."
            )


        # ----------------------------------------------------
        # OPEN WOLF FOLDER
        # ----------------------------------------------------

        if (
            "open wolf folder" in text
            or "open folder" in text
            or "open wolf files" in text
        ):

            if self.open_file(WOLF_FOLDER):

                return (
                    "Opening the WOLF OS folder. 📁"
                )

            return (
                "I couldn't open the WOLF OS folder."
            )


        # ----------------------------------------------------
        # OPEN WOLF OS
        # ----------------------------------------------------

        if (
            "open wolf os" in text
            or text == "wolf os"
        ):

            launcher = os.path.join(
                WOLF_FOLDER,
                "wolf_launcher.py"
            )

            try:

                subprocess.Popen([
                    "/usr/local/bin/python3.14",
                    launcher
                ])

                return (
                    "Launching WOLF OS. 🐺💻"
                )

            except Exception:

                return (
                    "I couldn't launch WOLF OS."
                )


        # ----------------------------------------------------
        # GAMES
        # ----------------------------------------------------

        if (
            "open games" in text
            or text == "games"
        ):

            return (
                "🎮 Games module detected.\n\n"
                "The WOLF OS Games system isn't "
                "installed yet.\n\n"
                "That's our next major module."
            )


        # ----------------------------------------------------
        # WHO ARE YOU
        # ----------------------------------------------------

        if (
            "who are you" in text
            or "what are you" in text
        ):

            return (
                "I am WOLF. 🐺\n\n"
                "I am the main AI of WOLF OS.\n\n"
                "My mission is to help control "
                "and operate the system."
            )


        # ----------------------------------------------------
        # WOLF
        # ----------------------------------------------------

        if "wolf" in text:

            return (
                "🐺 WOLF is listening."
            )


        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        return (
            "I understand what you said, "
            "but I don't have that ability yet.\n\n"
            "My command system is still growing. "
            "🐺⚙️"
        )


# ============================================================
# START WOLF
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WolfAI(root)

    root.mainloop()

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import time
import threading


class VoltAI:

    def __init__(self, root):

        self.root = root

        self.root.title("VOLT AI")
        self.root.geometry("900x700")
        self.root.configure(bg="#07111F")

        self.build_interface()

        self.add_message(
            "VOLT",
            "Automation systems online."
        )

        self.add_message(
            "VOLT",
            "I am VOLT, the automation and command AI."
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
            pady=(20, 5)
        )

        title = tk.Label(
            header,
            text="⚡ VOLT AI",
            font=("Arial", 28, "bold"),
            fg="#FFFFFF",
            bg="#07111F"
        )

        title.pack(side="left")

        status = tk.Label(
            header,
            text="● ONLINE",
            font=("Arial", 12, "bold"),
            fg="#4CFF88",
            bg="#07111F"
        )

        status.pack(
            side="right",
            padx=10
        )

        subtitle = tk.Label(
            self.root,
            text="AUTOMATION • COMMANDS • SYSTEM CONTROL",
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
            side="left"
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
            "VOLT",
            response
        )

        self.speak(
            response
        )

    # ---------------------------------------------------------
    # COMMAND HANDLER
    # ---------------------------------------------------------

    def handle_command(self, command):

        text = command.lower().strip()

        # -----------------------------------------------------
        # IDENTITY
        # -----------------------------------------------------

        if (
            "who are you" in text
            or "what are you" in text
        ):

            return (
                "I am VOLT AI, the automation and "
                "command system of WOLF OS."
            )

        # -----------------------------------------------------
        # GREETINGS
        # -----------------------------------------------------

        if text in [
            "hello",
            "hi",
            "hey"
        ]:

            return (
                "Hello. VOLT systems are online."
            )

        # -----------------------------------------------------
        # HELP
        # -----------------------------------------------------

        if (
            "help" in text
            or "what can you do" in text
        ):

            return (
                "I can open applications, folders and "
                "system tools, control common WOLF OS "
                "tasks, and execute safe automation commands."
            )

        # -----------------------------------------------------
        # TIME
        # -----------------------------------------------------

        if "time" in text:

            return time.strftime(
                "The current time is %I:%M %p."
            )

        # -----------------------------------------------------
        # OPEN SAFARI
        # -----------------------------------------------------

        if (
            "open safari" in text
            or "launch safari" in text
        ):

            subprocess.Popen(
                ["open", "-a", "Safari"]
            )

            return "Safari opened."

        # -----------------------------------------------------
        # OPEN TERMINAL
        # -----------------------------------------------------

        if (
            "open terminal" in text
            or "launch terminal" in text
        ):

            subprocess.Popen(
                ["open", "-a", "Terminal"]
            )

            return "Terminal opened."

        # -----------------------------------------------------
        # OPEN FINDER
        # -----------------------------------------------------

        if (
            "open finder" in text
            or "launch finder" in text
        ):

            subprocess.Popen(
                ["open", "-a", "Finder"]
            )

            return "Finder opened."

        # -----------------------------------------------------
        # OPEN MUSIC
        # -----------------------------------------------------

        if (
            "open music" in text
            or "launch music" in text
        ):

            subprocess.Popen(
                ["open", "-a", "Music"]
            )

            return "Music opened."

        # -----------------------------------------------------
        # OPEN CALCULATOR
        # -----------------------------------------------------

        if (
            "open calculator" in text
            or "launch calculator" in text
        ):

            subprocess.Popen(
                ["open", "-a", "Calculator"]
            )

            return "Calculator opened."

        # -----------------------------------------------------
        # OPEN SETTINGS
        # -----------------------------------------------------

        if (
            "open settings" in text
            or "system settings" in text
        ):

            subprocess.Popen(
                ["open", "x-apple.systempreferences:"]
            )

            return "System Settings opened."

        # -----------------------------------------------------
        # OPEN DOWNLOADS
        # -----------------------------------------------------

        if "open downloads" in text:

            subprocess.Popen(
                [
                    "open",
                    os.path.expanduser("~/Downloads")
                ]
            )

            return "Downloads opened."

        # -----------------------------------------------------
        # OPEN DESKTOP
        # -----------------------------------------------------

        if "open desktop" in text:

            subprocess.Popen(
                [
                    "open",
                    os.path.expanduser("~/Desktop")
                ]
            )

            return "Desktop opened."

        # -----------------------------------------------------
        # OPEN DOCUMENTS
        # -----------------------------------------------------

        if "open documents" in text:

            subprocess.Popen(
                [
                    "open",
                    os.path.expanduser("~/Documents")
                ]
            )

            return "Documents opened."

        # -----------------------------------------------------
        # OPEN WOLF OS
        # -----------------------------------------------------

        if (
            "open wolf os" in text
            or "open wolf folder" in text
        ):

            subprocess.Popen(
                [
                    "open",
                    os.path.expanduser("~/WolfOS")
                ]
            )

            return "WOLF OS folder opened."

        # -----------------------------------------------------
        # WOLF OS
        # -----------------------------------------------------

        if (
            "launch wolf os" in text
            or "start wolf os" in text
        ):

            launcher = os.path.expanduser(
                "~/WolfOS/wolf_launcher.py"
            )

            if os.path.exists(launcher):

                subprocess.Popen(
                    [
                        "/usr/local/bin/python3.14",
                        launcher
                    ]
                )

                return "Launching WOLF OS."

            return "I could not find the WOLF OS launcher."

        # -----------------------------------------------------
        # OPEN NOTES
        # -----------------------------------------------------

        if (
            "open notes" in text
            or "launch notes" in text
        ):

            notes = os.path.expanduser(
                "~/WolfOS/wolf_note.txt"
            )

            if not os.path.exists(notes):

                open(
                    notes,
                    "w"
                ).close()

            subprocess.Popen(
                [
                    "open",
                    notes
                ]
            )

            return "WOLF notes opened."

        # -----------------------------------------------------
        # BATTERY
        # -----------------------------------------------------

        if "battery" in text:

            try:

                result = subprocess.check_output(
                    ["pmset", "-g", "batt"],
                    text=True
                )

                return result.strip()

            except Exception:

                return "I could not check the battery."

        # -----------------------------------------------------
        # FINDER HOME
        # -----------------------------------------------------

        if (
            "open home folder" in text
            or "open home" in text
        ):

            subprocess.Popen(
                [
                    "open",
                    os.path.expanduser("~")
                ]
            )

            return "Home folder opened."

        # -----------------------------------------------------
        # RESTART WOLF
        # -----------------------------------------------------

        if (
            "restart wolf" in text
            or "restart wolf os" in text
        ):

            return (
                "Restart command recognized. "
                "Automatic restart will be added to VOLT later."
            )

        # -----------------------------------------------------
        # DEFAULT
        # -----------------------------------------------------

        return (
            "I understand the command, but that automation "
            "has not been added yet."
        )

    # ---------------------------------------------------------
    # SPEECH
    # ---------------------------------------------------------

    def speak(self, text):

        def speech():

            try:

                subprocess.run(
                    ["say", text],
                    check=False
                )

            except Exception:

                pass

        threading.Thread(
            target=speech,
            daemon=True
        ).start()


# -------------------------------------------------------------
# START VOLT
# -------------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = VoltAI(
        root
    )

    root.mainloop()

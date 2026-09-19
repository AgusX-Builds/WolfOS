import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import platform
import os
import shutil
import time


class AegisAI:

    def __init__(self, root):

        self.root = root

        self.root.title("AEGIS AI")
        self.root.geometry("900x700")
        self.root.configure(bg="#07111F")

        self.build_interface()

        self.add_message(
            "AEGIS",
            "Security systems online."
        )

        self.add_message(
            "AEGIS",
            "I am AEGIS, the security and system-monitoring AI of WOLF OS."
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
            text="🛡️ AEGIS AI",
            font=("Arial", 28, "bold"),
            fg="#FFFFFF",
            bg="#07111F"
        )

        title.pack(side="left")

        status = tk.Label(
            header,
            text="● SECURE",
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
            text="SECURITY • SYSTEM MONITORING • DIAGNOSTICS",
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
            "AEGIS",
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
                "I am AEGIS AI, the security and "
                "system-monitoring AI of WOLF OS."
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
                "Hello. AEGIS security systems are online."
            )

        # -----------------------------------------------------
        # HELP
        # -----------------------------------------------------

        if (
            "help" in text
            or "what can you do" in text
        ):

            return (
                "I can check system information, battery status, "
                "disk space, memory information, network status, "
                "running processes, and WOLF OS files."
            )

        # -----------------------------------------------------
        # TIME
        # -----------------------------------------------------

        if "time" in text:

            return time.strftime(
                "The current time is %I:%M %p."
            )

        # -----------------------------------------------------
        # SYSTEM INFORMATION
        # -----------------------------------------------------

        if (
            "system information" in text
            or "system info" in text
            or "computer information" in text
            or "computer info" in text
        ):

            return self.system_information()

        # -----------------------------------------------------
        # BATTERY
        # -----------------------------------------------------

        if "battery" in text:

            return self.check_battery()

        # -----------------------------------------------------
        # DISK SPACE
        # -----------------------------------------------------

        if (
            "disk space" in text
            or "storage" in text
            or "hard drive" in text
        ):

            return self.check_disk()

        # -----------------------------------------------------
        # MEMORY
        # -----------------------------------------------------

        if (
            "memory" in text
            or "ram" in text
        ):

            return self.check_memory()

        # -----------------------------------------------------
        # NETWORK
        # -----------------------------------------------------

        if (
            "network" in text
            or "internet" in text
            or "connection" in text
        ):

            return self.check_network()

        # -----------------------------------------------------
        # PROCESSES
        # -----------------------------------------------------

        if (
            "running processes" in text
            or "processes" in text
            or "what is running" in text
        ):

            return self.check_processes()

        # -----------------------------------------------------
        # WOLF OS STATUS
        # -----------------------------------------------------

        if (
            "wolf status" in text
            or "wolf os status" in text
        ):

            return self.wolf_status()

        # -----------------------------------------------------
        # WOLF FILES
        # -----------------------------------------------------

        if (
            "wolf files" in text
            or "wolf os files" in text
        ):

            return self.check_wolf_files()

        # -----------------------------------------------------
        # OPEN SYSTEM SETTINGS
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
        # OPEN ACTIVITY MONITOR
        # -----------------------------------------------------

        if (
            "activity monitor" in text
            or "open activity monitor" in text
        ):

            subprocess.Popen(
                ["open", "-a", "Activity Monitor"]
            )

            return "Activity Monitor opened."

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
        # DEFAULT
        # -----------------------------------------------------

        return (
            "I understand the command, but that security "
            "function has not been added yet."
        )

    # ---------------------------------------------------------
    # SYSTEM INFORMATION
    # ---------------------------------------------------------

    def system_information(self):

        try:

            system = platform.system()
            version = platform.mac_ver()[0]
            machine = platform.machine()
            processor = platform.processor()

            return (
                f"System: {system}\n"
                f"macOS version: {version}\n"
                f"Architecture: {machine}\n"
                f"Processor: {processor}"
            )

        except Exception as error:

            return (
                f"I could not read system information: {error}"
            )

    # ---------------------------------------------------------
    # BATTERY
    # ---------------------------------------------------------

    def check_battery(self):

        try:

            result = subprocess.check_output(
                ["pmset", "-g", "batt"],
                text=True
            )

            return result.strip()

        except Exception:

            return (
                "I could not read the battery status."
            )

    # ---------------------------------------------------------
    # DISK
    # ---------------------------------------------------------

    def check_disk(self):

        try:

            total, used, free = shutil.disk_usage("/")

            total_gb = total / (1024 ** 3)
            used_gb = used / (1024 ** 3)
            free_gb = free / (1024 ** 3)

            return (
                f"Disk status:\n"
                f"Total: {total_gb:.1f} GB\n"
                f"Used: {used_gb:.1f} GB\n"
                f"Free: {free_gb:.1f} GB"
            )

        except Exception as error:

            return (
                f"I could not check disk space: {error}"
            )

    # ---------------------------------------------------------
    # MEMORY
    # ---------------------------------------------------------

    def check_memory(self):

        try:

            result = subprocess.check_output(
                [
                    "vm_stat"
                ],
                text=True
            )

            return (
                "Memory information:\n\n"
                + result
            )

        except Exception as error:

            return (
                f"I could not check memory: {error}"
            )

    # ---------------------------------------------------------
    # NETWORK
    # ---------------------------------------------------------

    def check_network(self):

        try:

            result = subprocess.run(
                [
                    "networksetup",
                    "-getinfo",
                    "Wi-Fi"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                return (
                    "Wi-Fi network information:\n\n"
                    + result.stdout.strip()
                )

            return (
                "I could not retrieve Wi-Fi information."
            )

        except Exception as error:

            return (
                f"I could not check the network: {error}"
            )

    # ---------------------------------------------------------
    # PROCESSES
    # ---------------------------------------------------------

    def check_processes(self):

        try:

            result = subprocess.check_output(
                [
                    "ps",
                    "-axo",
                    "pid,comm,%cpu,%mem"
                ],
                text=True
            )

            lines = result.strip().splitlines()

            important = lines[:11]

            return (
                "Top running processes:\n\n"
                + "\n".join(important)
            )

        except Exception as error:

            return (
                f"I could not read running processes: {error}"
            )

    # ---------------------------------------------------------
    # WOLF STATUS
    # ---------------------------------------------------------

    def wolf_status(self):

        wolf_folder = os.path.expanduser(
            "~/WolfOS"
        )

        if not os.path.exists(wolf_folder):

            return "WOLF OS folder was not found."

        files = os.listdir(
            wolf_folder
        )

        python_files = [
            file
            for file in files
            if file.endswith(".py")
        ]

        return (
            "WOLF OS status: ONLINE\n"
            f"WOLF folder: FOUND\n"
            f"Python modules: {len(python_files)}"
        )

    # ---------------------------------------------------------
    # WOLF FILES
    # ---------------------------------------------------------

    def check_wolf_files(self):

        wolf_folder = os.path.expanduser(
            "~/WolfOS"
        )

        if not os.path.exists(wolf_folder):

            return "WOLF OS folder was not found."

        files = sorted(
            os.listdir(wolf_folder)
        )

        if not files:

            return "The WOLF OS folder is empty."

        return (
            "WOLF OS files:\n\n"
            + "\n".join(files)
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
# START AEGIS
# -------------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = AegisAI(
        root
    )

    root.mainloop()

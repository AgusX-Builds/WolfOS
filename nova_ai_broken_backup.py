import tkinter as tk
from tkinter import scrolledtext
import datetime
import subprocess
import threading

class NovaAI:

```
def __init__(self, root):

    self.root = root

    self.root.title("NOVA AI")
    self.root.geometry("850x650")
    self.root.minsize(700, 550)
    self.root.configure(bg="#07111F")

    self.create_interface()

    self.add_message(
        "NOVA",
        "NOVA online. Intelligence and planning systems ready."
    )

# --------------------------------------------------
# Interface
# --------------------------------------------------

def create_interface(self):

    header = tk.Frame(
        self.root,
        bg="#07111F"
    )

    header.pack(
        fill="x",
        padx=25,
        pady=20
    )

    title = tk.Label(
        header,
        text="🧠 NOVA",
        font=("Arial", 28, "bold"),
        fg="white",
        bg="#07111F"
    )

    title.pack()

    subtitle = tk.Label(
        header,
        text="INTELLIGENCE • PLANNING • PROBLEM SOLVING",
        font=("Arial", 10, "bold"),
        fg="#8fa3b8",
        bg="#07111F"
    )

    subtitle.pack(
        pady=(5, 0)
    )

    status = tk.Label(
        header,
        text="● ONLINE",
        font=("Arial", 10, "bold"),
        fg="#39ff88",
        bg="#07111F"
    )

    status.pack(
        pady=(8, 0)
    )

    # --------------------------------------------------
    # Chat
    # --------------------------------------------------

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
        padx=25,
        pady=10
    )

    self.chat.configure(
        state="disabled"
    )

    # --------------------------------------------------
    # Input
    # --------------------------------------------------

    bottom = tk.Frame(
        self.root,
        bg="#07111F"
    )

    bottom.pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

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
        lambda event: self.send_message()
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
        command=self.send_message
    )

    send_button.pack(
        side="left"
    )

# --------------------------------------------------
# Chat
# --------------------------------------------------

def add_message(self, speaker, message):

    self.chat.configure(
        state="normal"
    )

    self.chat.insert(
        tk.END,
        f"{speaker}: {message}\n\n"
    )

    self.chat.see(
        tk.END
    )

    self.chat.configure(
        state="disabled"
    )

# --------------------------------------------------
# Send
# --------------------------------------------------

def send_message(self):

    text = self.entry.get().strip()

    if not text:
        return

    self.entry.delete(
        0,
        tk.END
    )

    self.add_message(
        "YOU",
        text
    )

    response = self.get_response(
        text
    )

    self.add_message(
        "NOVA",
        response
    )

# --------------------------------------------------
# NOVA intelligence
# --------------------------------------------------

def get_response(self, text):

    lower = text.lower().strip()

    # Greetings
    if any(
        word in lower
        for word in [
            "hello",
            "hi",
            "hey",
            "hola"
        ]
    ):
        return (
            "Hello. I am NOVA, the intelligence system "
            "of the WOLF AI network."
        )

    # Identity
    if "who are you" in lower:
        return (
            "I am NOVA. My role is intelligence, "
            "planning, analysis, and problem solving."
        )

    # Help
    if (
        "help" in lower
        or "what can you do" in lower
    ):
        return (
            "I can help break problems into steps, "
            "plan projects, explain concepts, "
            "organize ideas, and analyze problems."
        )

    # Time
    if (
        "what time" in lower
        or lower == "time"
    ):
        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"The current time is {current_time}."
        )

    # Date
    if (
        "what date" in lower
        or lower == "date"
        or "what day is it" in lower
    ):
        current_date = datetime.datetime.now().strftime(
            "%A, %B %d, %Y"
        )

        return (
            f"Today is {current_date}."
        )

    # Planning
    if (
        "plan" in lower
        or "planning" in lower
        or "how should i" in lower
        or "how do i" in lower
    ):
        return (
            "Let's approach it systematically.\n\n"
            "1. Define the goal.\n"
            "2. Identify what we already have.\n"
            "3. Break the goal into smaller tasks.\n"
            "4. Complete and test each task.\n"
            "5. Review the result and improve it."
        )

    # Project
    if (
        "project" in lower
        or "build" in lower
        or "make" in lower
    ):
        return (
            "For a project, I recommend three stages: "
            "design, build, and test. Tell me what you "
            "want to build and I can help turn it into "
            "a step-by-step plan."
        )

    # Programming
    if (
        "python" in lower
        or "programming" in lower
        or "code" in lower
        or "coding" in lower
    ):
        return (
            "I can help you understand programming "
            "concepts, design a program, find errors, "
            "and organize code into manageable steps."
        )

    # Problem solving
    if (
        "problem" in lower
        or "error" in lower
        or "bug" in lower
        or "stuck" in lower
    ):
        return (
            "Let's diagnose it. First identify what "
            "you expected to happen, then what actually "
            "happened, and finally the exact error or "
            "unexpected behavior."
        )

    # Ideas
    if (
        "idea" in lower
        or "ideas" in lower
    ):
        return (
            "I can brainstorm with you. Give me the "
            "project or topic, and we can generate "
            "several possible ideas and organize them."
        )

    # WOLF OS
    if (
        "wolf os" in lower
        or "wolf" in lower
    ):
        return (
            "WOLF is the central AI. I am NOVA, "
            "the intelligence specialist. Together "
            "we form part of the WOLF AI network."
        )

    # Goodbye
    if (
        "bye" in lower
        or "goodbye" in lower
    ):
        return (
            "NOVA standing by. See you later."
        )

    # Default
    return (
        "Interesting. Give me more details and I can "
        "break the problem down, organize the information, "
        "and help you create a plan."
    )
```

root = tk.Tk()

app = NovaAI(
root
)

root.mainloop()


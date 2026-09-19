import tkinter as tk
from tkinter import scrolledtext
import datetime
import ast
import operator


class NovaAI:

    def __init__(self, root):
        self.root = root

        root.title("NOVA AI")
        root.geometry("900x700")
        root.configure(bg="#07111F")

        header = tk.Frame(root, bg="#07111F")
        header.pack(fill="x", padx=25, pady=(20, 10))

        tk.Label(
            header,
            text="🧠 NOVA",
            font=("Arial", 30, "bold"),
            fg="white",
            bg="#07111F"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="INTELLIGENCE • PLANNING • PROBLEM SOLVING",
            font=("Arial", 11),
            fg="#7FA8C9",
            bg="#07111F"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="● ONLINE",
            font=("Arial", 10, "bold"),
            fg="#55DD88",
            bg="#07111F"
        ).pack(anchor="w", pady=(6, 0))

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="#0B1B2D",
            fg="white",
            insertbackground="white",
            relief="flat",
            padx=15,
            pady=15
        )
        self.chat.pack(fill="both", expand=True, padx=25, pady=10)

        self.chat.insert(
            tk.END,
            "NOVA: Online.\n"
            "NOVA: Intelligence and planning systems ready.\n"
            "NOVA: Tell me what you want to build, solve, learn, or plan.\n\n"
        )

        bottom = tk.Frame(root, bg="#07111F")
        bottom.pack(fill="x", padx=25, pady=(5, 20))

        self.entry = tk.Entry(
            bottom,
            font=("Arial", 13),
            bg="#10253A",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=12)
        self.entry.bind("<Return>", self.send_message)

        tk.Button(
            bottom,
            text="SEND",
            command=self.send_message,
            font=("Arial", 11, "bold"),
            bg="#173B5C",
            fg="white",
            activebackground="#245B87",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side="right", padx=(10, 0))

        self.entry.focus()

    def send_message(self, event=None):
        message = self.entry.get().strip()

        if not message:
            return

        self.chat.insert(tk.END, f"YOU: {message}\n")

        response = self.think(message)

        self.chat.insert(tk.END, f"NOVA: {response}\n\n")
        self.chat.see(tk.END)

        self.entry.delete(0, tk.END)

    def think(self, message):
        text = message.lower().strip()

        # Greetings
        if any(x in text for x in [
            "hello", "hi", "hey", "hola"
        ]):
            return (
                "Hello. I am ready. "
                "What are we working on?"
            )

        # Identity
        if "who are you" in text or "what are you" in text:
            return (
                "I am NOVA, the Intelligence and Planning AI of WOLF OS. "
                "I specialize in planning, reasoning, learning, programming, "
                "and solving problems."
            )

        # WOLF
        if "wolf os" in text:
            return (
                "WOLF OS is our desktop operating environment. "
                "WOLF is the main AI coordinator, while I handle intelligence "
                "and planning tasks."
            )

        if "who is wolf" in text:
            return (
                "WOLF is the main AI of WOLF OS. "
                "I am NOVA, one of WOLF's specialized AI systems."
            )

        # Help
        if text == "help" or "what can you do" in text:
            return (
                "I can help you with:\n"
                "• Project planning\n"
                "• Programming\n"
                "• Debugging\n"
                "• Learning\n"
                "• Game design\n"
                "• WOLF OS development\n"
                "• Ideas and inventions\n"
                "• Breaking difficult problems into steps"
            )

        # Time
        if "time" in text:
            return datetime.datetime.now().strftime(
                "The current time is %I:%M %p."
            )

        # Date
        if "date" in text or "today" in text:
            return datetime.datetime.now().strftime(
                "Today is %A, %B %d, %Y."
            )

        # Planning
        if any(x in text for x in [
            "make a plan",
            "create a plan",
            "plan this",
            "planning",
            "plan for"
        ]):
            return (
                "Let's structure it like this:\n\n"
                "1. Define the goal.\n"
                "2. List the important features.\n"
                "3. Break the work into small tasks.\n"
                "4. Build the first task.\n"
                "5. Test it.\n"
                "6. Fix problems.\n"
                "7. Add improvements.\n\n"
                "Give me the project and I can turn it into a detailed plan."
            )

        # Project building
        if any(x in text for x in [
            "build a project",
            "start a project",
            "new project",
            "build something",
            "create something"
        ]):
            return (
                "Good. Before building it, we should define four things:\n\n"
                "GOAL → FEATURES → FILE STRUCTURE → BUILD STEPS\n\n"
                "Tell me what you want to create and I will organize it."
            )

        # Programming
        if any(x in text for x in [
            "python",
            "programming",
            "program",
            "coding",
            "code"
        ]):
            return (
                "I can help with programming. "
                "Tell me what the program should do, what language you're using, "
                "and any error you see. I can then break the solution into steps."
            )

        # Errors
        if any(x in text for x in [
            "error",
            "bug",
            "broken",
            "doesn't work",
            "doesnt work",
            "not working",
            "stuck"
        ]):
            return (
                "Let's debug it systematically.\n\n"
                "1. Find the exact error.\n"
                "2. Identify the file and line.\n"
                "3. Determine what the program expected.\n"
                "4. Fix the underlying cause.\n"
                "5. Run it again.\n\n"
                "Send me the exact error message."
            )

        # Game design
        if any(x in text for x in [
            "make a game",
            "create a game",
            "game idea",
            "game"
        ]):
            return (
                "For a game, we should define:\n\n"
                "• Genre\n"
                "• Player\n"
                "• World\n"
                "• Controls\n"
                "• Enemies\n"
                "• Items\n"
                "• Progression\n"
                "• Missions\n"
                "• Save system\n\n"
                "Give me your game idea and we can design it."
            )

        # Learning
        if any(x in text for x in [
            "teach me",
            "learn",
            "lesson",
            "explain"
        ]):
            return (
                "Absolutely. Tell me the subject and your current level. "
                "I can explain it step by step and then give you a small challenge "
                "to test what you learned."
            )

        # Ideas
        if "idea" in text or "ideas" in text:
            return (
                "Give me the idea exactly as you imagined it. "
                "It doesn't have to be finished. "
                "I'll help turn it into a structured concept."
            )

        # Calculate
        if text.startswith("calculate "):
            expression = text.replace("calculate ", "", 1).strip()
            return self.calculate(expression)

        # Goodbye
        if any(x in text for x in [
            "bye",
            "goodbye",
            "see you"
        ]):
            return "NOVA standing by. I'll be here when you need me."

        # General intelligent fallback
        return (
            "Interesting. Let's break that down.\n\n"
            "First, identify the exact goal.\n"
            "Then determine what information or tools are needed.\n"
            "Next, divide the task into smaller steps.\n"
            "Finally, test the result and improve it.\n\n"
            "Tell me more about what you're trying to accomplish."
        )

    def calculate(self, expression):
        try:
            tree = ast.parse(expression, mode="eval")
            result = self.safe_eval(tree.body)
            return f"The answer is {result}."
        except Exception:
            return (
                "I couldn't safely calculate that. "
                "Try something simple like: calculate 25 * 4"
            )

    def safe_eval(self, node):

        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod
        }

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError()

        if isinstance(node, ast.BinOp):
            operation = operations.get(type(node.op))

            if operation is None:
                raise ValueError()

            left = self.safe_eval(node.left)
            right = self.safe_eval(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            value = self.safe_eval(node.operand)

            if isinstance(node.op, ast.USub):
                return -value

            if isinstance(node.op, ast.UAdd):
                return value

        raise ValueError()


root = tk.Tk()
app = NovaAI(root)
root.mainloop()

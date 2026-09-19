import os
import sys
import datetime
import textwrap

# ============================================================
# NOVA AI v2
# WOLF OS Intelligence
# ============================================================

VERSION = "2.0"

conversation = []

WOLF_CONTEXT = """
You are NOVA, the AI assistant inside WOLF OS.

WOLF OS is a custom desktop operating system project built in Python.
The user is actively developing it and wants to add useful applications,
games, tools, and AI features.

You should act like a helpful technical AI assistant.

Your main abilities are:
- programming help
- debugging
- project planning
- explaining technical concepts
- brainstorming features
- organizing projects
- helping develop WOLF OS
- helping develop the user's games and other projects

Be friendly, clear, practical, and concise.

When helping with programming:
1. Explain what is wrong.
2. Explain what the solution does.
3. Give complete code when appropriate.
4. Avoid unnecessarily complicated solutions.
5. Prefer solutions that work on macOS and Python 3.14.

Never pretend that you executed something if you did not.
Never claim to have access to files unless the user provides them.
"""

def slow_print(text):
    """Print text in a readable way."""
    print()
    for paragraph in text.split("\n"):
        print(textwrap.fill(paragraph, width=85))
    print()


def show_help():
    print("""
╔══════════════════════════════════════════════╗
║                 NOVA COMMANDS                ║
╠══════════════════════════════════════════════╣
║ help       Show this menu                    ║
║ plan       Project planning mode             ║
║ code       Coding mode                       ║
║ wolf       WOLF OS information               ║
║ clear      Clear conversation memory         ║
║ status     Show NOVA status                  ║
║ time       Show current time                 ║
║ exit       Close NOVA                        ║
╚══════════════════════════════════════════════╝
""")


def wolf_info():
    slow_print("""
WOLF OS is the main project connected to NOVA.

Current goals include:
- desktop-style operating system
- applications
- games
- custom WOLF branding
- a launcher that opens the latest WOLF OS
- future integration between WOLF OS and NOVA

NOVA can act as the intelligence layer for WOLF OS.
""")


def show_status():
    print("\nNOVA STATUS")
    print("───────────")
    print(f"Version: {VERSION}")
    print("System: WOLF OS")
    print("Python:", sys.version.split()[0])
    print("Conversation memory:", len(conversation), "messages")
    print("Status: ONLINE\n")


def show_time():
    now = datetime.datetime.now()
    print("\nCurrent time:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print()


def clear_memory():
    conversation.clear()
    print("\nNOVA memory cleared.\n")


def planning_mode():
    print("""
╔══════════════════════════════════════════════╗
║              NOVA PLANNING MODE              ║
╚══════════════════════════════════════════════╝

Tell me what you want to build.

Example:
"Make a game for WOLF OS"

I'll help break the idea into:
1. Goal
2. Features
3. Files
4. Development steps
5. Testing
6. Future upgrades
""")

    idea = input("PLAN > ").strip()

    if not idea:
        return

    slow_print(
        f"""Project idea received:

{idea}

Suggested development process:

1. Define the main goal.
2. Break the project into smaller systems.
3. Decide which files are needed.
4. Build the simplest working version.
5. Test each system.
6. Add visual improvements.
7. Connect the project to WOLF OS.
8. Add future upgrades.

This keeps the project manageable instead of trying to build everything at once."""
    )


def coding_mode():
    print("""
╔══════════════════════════════════════════════╗
║                NOVA CODING MODE              ║
╚══════════════════════════════════════════════╝

Describe the programming problem.

Example:
"My Python program crashes when I click a button."

NOVA will help analyze the problem and plan the fix.
""")

    problem = input("CODE > ").strip()

    if not problem:
        return

    slow_print(
        f"""Programming problem:

{problem}

Recommended debugging process:

1. Find the exact error message.
2. Identify which file caused it.
3. Locate the line where it happened.
4. Determine what the program expected.
5. Fix the underlying problem.
6. Run the program again.
7. Test the feature that caused the problem."""
    )


def think(user_input):
    """
    Basic local reasoning engine.

    This version does not require an online AI API.
    It provides structured responses and can later be replaced
    with a real AI backend.
    """

    lower = user_input.lower()

    # Greetings
    if any(word in lower for word in ["hello", "hi", "hey", "hola"]):
        return (
            "Hello! I'm NOVA, the intelligence system for WOLF OS. "
            "What are we building today?"
        )

    # Identity
    if "who are you" in lower or "what are you" in lower:
        return (
            "I'm NOVA v2, the AI assistant we're building for WOLF OS. "
            "Right now I'm a local assistant, and we're preparing her "
            "for deeper WOLF OS integration."
        )

    # WOLF OS
    if "wolf os" in lower:
        return (
            "WOLF OS is the operating-system project we're developing. "
            "My job is to eventually become its built-in AI assistant."
        )

    # Programming
    if any(word in lower for word in [
        "python",
        "code",
        "program",
        "script",
        "error",
        "bug"
    ]):
        return (
            "This sounds like a programming task. "
            "Tell me the goal, the code you're using, and any error message. "
            "I can then break the problem into steps and help build the fix."
        )

    # Games
    if any(word in lower for word in [
        "game",
        "gaming",
        "games"
    ]):
        return (
            "For a game project, I'd recommend building it in systems: "
            "player, world, controls, UI, enemies, saving, and progression. "
            "We can build one working system at a time."
        )

    # Building
    if any(word in lower for word in [
        "build",
        "make",
        "create",
        "develop"
    ]):
        return (
            "Let's turn that idea into a project. "
            "First we'll define the goal, then split it into smaller "
            "features and build the first working version."
        )

    # Default
    return (
        "I understand. Let's work through it step by step. "
        "Tell me what you want NOVA to accomplish and I'll help turn "
        "the idea into a concrete plan."
    )


def chat():
    print("""
╔══════════════════════════════════════════════════╗
║                                                  ║
║                 N O V A  v2.0                    ║
║                                                  ║
║              WOLF OS INTELLIGENCE                ║
║                                                  ║
╚══════════════════════════════════════════════════╝

NOVA is online.

Type "help" for commands.
Type "exit" to close NOVA.
""")

    while True:
        try:
            user_input = input("YOU > ").strip()

        except KeyboardInterrupt:
            print("\n\nNOVA shutting down.")
            break

        except EOFError:
            print("\n\nNOVA shutting down.")
            break

        if not user_input:
            continue

        command = user_input.lower()

        if command == "exit":
            print("\nNOVA: Shutting down. WOLF OS remains online. 🐺\n")
            break

        if command == "help":
            show_help()
            continue

        if command == "wolf":
            wolf_info()
            continue

        if command == "status":
            show_status()
            continue

        if command == "time":
            show_time()
            continue

        if command == "clear":
            clear_memory()
            continue

        if command == "plan":
            planning_mode()
            continue

        if command == "code":
            coding_mode()
            continue

        conversation.append({
            "user": user_input,
            "time": datetime.datetime.now().isoformat()
        })

        response = think(user_input)

        slow_print("NOVA: " + response)


if __name__ == "__main__":
    chat()

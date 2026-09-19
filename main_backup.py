import tkinter as tk
from datetime import datetime
import os

# ============================================================
# WOLF OS
# ============================================================

WIDTH = 1000
HEIGHT = 650
NOTE_FILE = "wolf_note.txt"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("🐺 WOLF OS")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)


# ============================================================
# DESKTOP
# ============================================================

desktop = tk.Frame(root, bg="#111111")
desktop.pack(expand=True, fill="both")


# ============================================================
# TOP BAR
# ============================================================

top_bar = tk.Frame(
    desktop,
    bg="#202020",
    height=50
)

top_bar.pack(
    side="top",
    fill="x"
)

title = tk.Label(
    top_bar,
    text="🐺 WOLF OS",
    font=("Arial", 18, "bold"),
    bg="#202020",
    fg="white"
)

title.pack(
    side="left",
    padx=15
)


# ============================================================
# CLOCK
# ============================================================

clock = tk.Label(
    top_bar,
    text="",
    font=("Arial", 14),
    bg="#202020",
    fg="white"
)

clock.pack(
    side="right",
    padx=15
)


def update_clock():
    clock.config(
        text=datetime.now().strftime("%H:%M:%S")
    )
    root.after(1000, update_clock)


update_clock()


# ============================================================
# CALCULATOR
# ============================================================

def open_calculator():

    calculator = tk.Toplevel(root)

    calculator.title("🧮 Calculadora")
    calculator.geometry("350x500")
    calculator.resizable(False, False)

    display = tk.Entry(
        calculator,
        font=("Arial", 24),
        justify="right"
    )

    display.pack(
        padx=15,
        pady=20,
        fill="x"
    )

    def press(value):

        if value == "C":

            display.delete(
                0,
                tk.END
            )

        elif value == "=":

            try:

                result = eval(
                    display.get()
                )

                display.delete(
                    0,
                    tk.END
                )

                display.insert(
                    0,
                    str(result)
                )

            except:

                display.delete(
                    0,
                    tk.END
                )

                display.insert(
                    0,
                    "Error"
                )

        else:

            display.insert(
                tk.END,
                value
            )

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]

    for row in buttons:

        row_frame = tk.Frame(
            calculator
        )

        row_frame.pack(
            expand=True,
            fill="both"
        )

        for button in row:

            tk.Button(
                row_frame,
                text=button,
                font=("Arial", 18),
                command=lambda value=button: press(value)
            ).pack(
                side="left",
                expand=True,
                fill="both",
                padx=2,
                pady=2
            )


# ============================================================
# NOTES
# ============================================================

def open_notes():

    notes = tk.Toplevel(root)

    notes.title("📝 WOLF Notes")
    notes.geometry("700x500")
    notes.resizable(True, True)

    # Make Notes the active window
    notes.lift()
    notes.attributes("-topmost", True)
    notes.after(
        100,
        lambda: notes.attributes("-topmost", False)
    )

    # --------------------------------------------------------
    # TEXT AREA
    # --------------------------------------------------------

    text = tk.Text(
        notes,
        font=("Arial", 16),
        wrap="word",
        undo=True,
        bg="white",
        fg="black",
        insertbackground="black",
        cursor="xterm"
    )

    text.pack(
        expand=True,
        fill="both",
        padx=10,
        pady=10
    )

    # --------------------------------------------------------
    # LOAD SAVED NOTE
    # --------------------------------------------------------

    if os.path.exists(NOTE_FILE):

        try:

            with open(
                NOTE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                saved_note = file.read()

            text.insert(
                "1.0",
                saved_note
            )

        except Exception as error:

            print(
                "Error loading note:",
                error
            )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save_note():

        content = text.get(
            "1.0",
            "end-1c"
        )

        try:

            with open(
                NOTE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

            status.config(
                text="✅ Nota guardada"
            )

        except Exception as error:

            status.config(
                text="❌ Error al guardar"
            )

            print(
                "Save error:",
                error
            )

    # --------------------------------------------------------
    # CLEAR
    # --------------------------------------------------------

    def clear_note():

        text.delete(
            "1.0",
            tk.END
        )

        status.config(
            text="🗑️ Nota borrada"
        )

    # --------------------------------------------------------
    # BUTTON BAR
    # --------------------------------------------------------

    bottom_bar = tk.Frame(
        notes,
        bg="#eeeeee"
    )

    bottom_bar.pack(
        side="bottom",
        fill="x",
        padx=10,
        pady=10
    )

    save_button = tk.Button(
        bottom_bar,
        text="💾 Guardar",
        font=("Arial", 12, "bold"),
        command=save_note
    )

    save_button.pack(
        side="left"
    )

    clear_button = tk.Button(
        bottom_bar,
        text="🗑️ Borrar",
        font=("Arial", 12),
        command=clear_note
    )

    clear_button.pack(
        side="left",
        padx=10
    )

    status = tk.Label(
        bottom_bar,
        text="Escribe tu nota...",
        font=("Arial", 11),
        bg="#eeeeee"
    )

    status.pack(
        side="left",
        padx=10
    )

    # --------------------------------------------------------
    # FORCE KEYBOARD FOCUS
    # --------------------------------------------------------

    notes.after(
        200,
        lambda: text.focus_force()
    )


# ============================================================
# FILE EXPLORER
# ============================================================

def open_files():

    files = tk.Toplevel(root)

    files.title("📁 Archivos")
    files.geometry("650x450")

    tk.Label(
        files,
        text="📁 Explorador de archivos",
        font=("Arial", 22, "bold")
    ).pack(
        pady=20
    )

    file_list = tk.Listbox(
        files,
        font=("Arial", 14)
    )

    file_list.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=10
    )

    # Show files in the WolfOS folder
    try:

        for filename in os.listdir("."):

            file_list.insert(
                tk.END,
                filename
            )

    except Exception as error:

        print(
            "File Explorer error:",
            error
        )


# ============================================================
# PROFILE
# ============================================================

def open_profile():

    profile = tk.Toplevel(root)

    profile.title("👤 Perfil")
    profile.geometry("400x350")

    tk.Label(
        profile,
        text="🐺",
        font=("Arial", 60)
    ).pack(
        pady=20
    )

    tk.Label(
        profile,
        text="Agus",
        font=("Arial", 24, "bold")
    ).pack()

    tk.Label(
        profile,
        text="Nivel 1\nXP: 0\nCoins: 0",
        font=("Arial", 14)
    ).pack(
        pady=15
    )


# ============================================================
# SETTINGS
# ============================================================

def open_settings():

    settings = tk.Toplevel(root)

    settings.title("⚙️ Configuración")
    settings.geometry("450x350")

    tk.Label(
        settings,
        text="⚙️ Configuración",
        font=("Arial", 24, "bold")
    ).pack(
        pady=30
    )

    tk.Label(
        settings,
        text="WOLF OS V3",
        font=("Arial", 14)
    ).pack(
        pady=10
    )

    tk.Button(
        settings,
        text="Cerrar",
        command=settings.destroy
    ).pack(
        pady=20
    )


# ============================================================
# GAME CENTER
# ============================================================

def open_games():

    games = tk.Toplevel(root)

    games.title("🎮 WOLF GAME CENTER")
    games.geometry("500x400")

    tk.Label(
        games,
        text="🎮 WOLF GAME CENTER",
        font=("Arial", 24, "bold")
    ).pack(
        pady=30
    )

    tk.Label(
        games,
        text="Tus juegos aparecerán aquí.",
        font=("Arial", 14)
    ).pack(
        pady=20
    )


# ============================================================
# WELCOME
# ============================================================

welcome = tk.Label(
    desktop,
    text="Bienvenido a WOLF OS",
    font=("Arial", 32, "bold"),
    bg="#111111",
    fg="white"
)

welcome.pack(
    pady=45
)

subtitle = tk.Label(
    desktop,
    text="Tu computadora. Tus reglas.",
    font=("Arial", 16),
    bg="#111111",
    fg="#aaaaaa"
)

subtitle.pack()


# ============================================================
# APPLICATIONS
# ============================================================

apps = tk.Frame(
    desktop,
    bg="#111111"
)

apps.pack(
    pady=35
)


def create_app_button(
    text,
    row,
    column,
    command
):

    button = tk.Button(
        apps,
        text=text,
        font=("Arial", 14),
        width=13,
        height=4,
        command=command
    )

    button.grid(
        row=row,
        column=column,
        padx=8,
        pady=8
    )


create_app_button(
    "🧮\nCalculadora",
    0,
    0,
    open_calculator
)

create_app_button(
    "📝\nNotas",
    0,
    1,
    open_notes
)

create_app_button(
    "📁\nArchivos",
    0,
    2,
    open_files
)

create_app_button(
    "👤\nPerfil",
    1,
    0,
    open_profile
)

create_app_button(
    "⚙️\nConfiguración",
    1,
    1,
    open_settings
)

create_app_button(
    "🎮\nJuegos",
    1,
    2,
    open_games
)


# ============================================================
# TASKBAR
# ============================================================

taskbar = tk.Frame(
    desktop,
    bg="#202020",
    height=55
)

taskbar.pack(
    side="bottom",
    fill="x"
)


start_button = tk.Button(
    taskbar,
    text="🐺 INICIO",
    font=("Arial", 12, "bold")
)

start_button.pack(
    side="left",
    padx=10,
    pady=10
)


shutdown_button = tk.Button(
    taskbar,
    text="⏻ Apagar",
    font=("Arial", 12),
    command=root.destroy
)

shutdown_button.pack(
    side="right",
    padx=10,
    pady=10
)


# ============================================================
# START
# ============================================================

root.mainloop()
import tkinter as tk
from datetime import datetime
import os

# ============================================================
# WOLF OS
# ============================================================

WIDTH = 1000
HEIGHT = 650

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
NOTE_FILE = os.path.join(PROJECT_FOLDER, "wolf_note.txt")


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

            display.delete(0, tk.END)

        elif value == "=":

            try:

                result = eval(display.get())

                display.delete(0, tk.END)
                display.insert(0, str(result))

            except:

                display.delete(0, tk.END)
                display.insert(0, "Error")

        else:

            display.insert(tk.END, value)

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"]
    ]

    for row in buttons:

        row_frame = tk.Frame(calculator)
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

    text = tk.Text(
        notes,
        font=("Arial", 16),
        wrap="word",
        undo=True,
        bg="white",
        fg="black",
        insertbackground="black"
    )

    text.pack(
        expand=True,
        fill="both",
        padx=10,
        pady=10
    )

    # LOAD

    if os.path.exists(NOTE_FILE):

        try:

            with open(
                NOTE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                text.insert(
                    "1.0",
                    file.read()
                )

        except Exception as error:

            print("Load error:", error)

    # SAVE

    def save_note():

        try:

            content = text.get(
                "1.0",
                "end-1c"
            )

            with open(
                NOTE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

            status.config(
                text="✅ GUARDADO"
            )

        except Exception as error:

            status.config(
                text="❌ ERROR"
            )

            print("SAVE ERROR:", error)

    # CLEAR

    def clear_note():

        text.delete(
            "1.0",
            tk.END
        )

        status.config(
            text="🗑️ Borrado"
        )

    bottom = tk.Frame(
        notes,
        bg="#eeeeee"
    )

    bottom.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Button(
        bottom,
        text="💾 GUARDAR",
        font=("Arial", 12, "bold"),
        command=save_note
    ).pack(
        side="left"
    )

    tk.Button(
        bottom,
        text="🗑️ BORRAR",
        command=clear_note
    ).pack(
        side="left",
        padx=10
    )

    status = tk.Label(
        bottom,
        text="Escribe una nota.",
        bg="#eeeeee"
    )

    status.pack(
        side="left",
        padx=10
    )

    text.focus_set()


# ============================================================
# TEXT FILE EDITOR
# ============================================================

def open_text_file(file_path):

    editor = tk.Toplevel(root)

    editor.title(
        "📝 " + os.path.basename(file_path)
    )

    editor.geometry("750x550")

    text = tk.Text(
        editor,
        font=("Arial", 15),
        wrap="word",
        undo=True,
        bg="white",
        fg="black",
        insertbackground="black"
    )

    text.pack(
        expand=True,
        fill="both",
        padx=10,
        pady=10
    )

    # LOAD

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text.insert(
                "1.0",
                file.read()
            )

    except Exception as error:

        text.insert(
            "1.0",
            "ERROR:\n\n" + str(error)
        )

    # SAVE

    def save_file():

        try:

            content = text.get(
                "1.0",
                "end-1c"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

            status.config(
                text="✅ Guardado"
            )

        except Exception as error:

            status.config(
                text="❌ Error"
            )

            print("SAVE ERROR:", error)

    bottom = tk.Frame(editor)

    bottom.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Button(
        bottom,
        text="💾 Guardar",
        font=("Arial", 12, "bold"),
        command=save_file
    ).pack(
        side="left"
    )

    status = tk.Label(
        bottom,
        text="Editando..."
    )

    status.pack(
        side="left",
        padx=15
    )

    text.focus_set()


# ============================================================
# FILE EXPLORER
# ============================================================

def open_files():

    files = tk.Toplevel(root)

    files.title("📁 WOLF File Explorer")
    files.geometry("750x550")

    current_path = PROJECT_FOLDER

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    tk.Label(
        files,
        text="📁 WOLF FILE EXPLORER",
        font=("Arial", 22, "bold")
    ).pack(
        pady=10
    )

    # --------------------------------------------------------
    # PATH
    # --------------------------------------------------------

    path_label = tk.Label(
        files,
        text="",
        font=("Arial", 10),
        anchor="w"
    )

    path_label.pack(
        fill="x",
        padx=15
    )

    # --------------------------------------------------------
    # TOOLBAR
    # --------------------------------------------------------

    toolbar = tk.Frame(files)

    toolbar.pack(
        fill="x",
        padx=10,
        pady=10
    )

    # --------------------------------------------------------
    # LIST
    # --------------------------------------------------------

    file_list = tk.Listbox(
        files,
        font=("Arial", 14)
    )

    file_list.pack(
        expand=True,
        fill="both",
        padx=15,
        pady=5
    )

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    def refresh():

        file_list.delete(
            0,
            tk.END
        )

        path_label.config(
            text=current_path
        )

        try:

            items = sorted(
                os.listdir(current_path),
                key=lambda name: (
                    not os.path.isdir(
                        os.path.join(
                            current_path,
                            name
                        )
                    ),
                    name.lower()
                )
            )

            for item in items:

                full_path = os.path.join(
                    current_path,
                    item
                )

                if os.path.isdir(full_path):

                    file_list.insert(
                        tk.END,
                        "📁 " + item
                    )

                else:

                    file_list.insert(
                        tk.END,
                        "📄 " + item
                    )

        except Exception as error:

            print(
                "Explorer error:",
                error
            )

    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    def go_back():

        nonlocal current_path

        parent = os.path.dirname(
            current_path
        )

        if (
            parent.startswith(PROJECT_FOLDER)
            and parent != current_path
        ):

            current_path = parent
            refresh()

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    def go_home():

        nonlocal current_path

        current_path = PROJECT_FOLDER
        refresh()

    # --------------------------------------------------------
    # OPEN
    # --------------------------------------------------------

    def open_selected(event=None):

        nonlocal current_path

        selection = file_list.curselection()

        if not selection:
            return

        displayed = file_list.get(
            selection[0]
        )

        item_name = displayed[2:]

        full_path = os.path.join(
            current_path,
            item_name
        )

        # Folder

        if os.path.isdir(full_path):

            current_path = full_path
            refresh()

            return

        # File

        if item_name.lower().endswith(
            (
                ".txt",
                ".py",
                ".md",
                ".json",
                ".csv"
            )
        ):

            open_text_file(
                full_path
            )

        else:

            print(
                "No puedo abrir este archivo:",
                item_name
            )

    # --------------------------------------------------------
    # NEW FILE
    # --------------------------------------------------------

    def new_file():

        window = tk.Toplevel(files)

        window.title("📄 Nuevo archivo")
        window.geometry("400x200")

        tk.Label(
            window,
            text="Nombre del archivo:",
            font=("Arial", 14)
        ).pack(
            pady=15
        )

        entry = tk.Entry(
            window,
            font=("Arial", 14)
        )

        entry.pack(
            padx=20,
            fill="x"
        )

        entry.focus_set()

        def create():

            filename = entry.get().strip()

            if not filename:
                return

            full_path = os.path.join(
                current_path,
                filename
            )

            try:

                with open(
                    full_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write("")

                window.destroy()
                refresh()

            except Exception as error:

                print(
                    "File creation error:",
                    error
                )

        tk.Button(
            window,
            text="Crear",
            font=("Arial", 12, "bold"),
            command=create
        ).pack(
            pady=20
        )

    # --------------------------------------------------------
    # NEW FOLDER
    # --------------------------------------------------------

    def new_folder():

        window = tk.Toplevel(files)

        window.title("📁 Nueva carpeta")
        window.geometry("400x200")

        tk.Label(
            window,
            text="Nombre de la carpeta:",
            font=("Arial", 14)
        ).pack(
            pady=15
        )

        entry = tk.Entry(
            window,
            font=("Arial", 14)
        )

        entry.pack(
            padx=20,
            fill="x"
        )

        entry.focus_set()

        def create():

            folder_name = entry.get().strip()

            if not folder_name:
                return

            full_path = os.path.join(
                current_path,
                folder_name
            )

            try:

                os.mkdir(full_path)

                window.destroy()
                refresh()

            except Exception as error:

                print(
                    "Folder creation error:",
                    error
                )

        tk.Button(
            window,
            text="Crear carpeta",
            font=("Arial", 12, "bold"),
            command=create
        ).pack(
            pady=20
        )

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    tk.Button(
        toolbar,
        text="⬅️ Atrás",
        command=go_back
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        toolbar,
        text="🏠 Inicio",
        command=go_home
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        toolbar,
        text="🔄 Actualizar",
        command=refresh
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        toolbar,
        text="📄 Nuevo archivo",
        command=new_file
    ).pack(
        side="right",
        padx=4
    )

    tk.Button(
        toolbar,
        text="📁 Nueva carpeta",
        command=new_folder
    ).pack(
        side="right",
        padx=4
    )

    file_list.bind(
        "<Double-Button-1>",
        open_selected
    )

    refresh()


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
        text="WOLF OS V5",
        font=("Arial", 14)
    ).pack()

    tk.Button(
        settings,
        text="Cerrar",
        command=settings.destroy
    ).pack(
        pady=20
    )


# ============================================================
# GAMES
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
    ).pack()


# ============================================================
# START MENU
# ============================================================

def open_start_menu():

    menu = tk.Toplevel(root)

    menu.title("🐺 WOLF START")
    menu.geometry("350x500")

    menu.configure(
        bg="#181818"
    )

    tk.Label(
        menu,
        text="🐺 WOLF",
        font=("Arial", 28, "bold"),
        bg="#181818",
        fg="white"
    ).pack(
        pady=20
    )

    tk.Label(
        menu,
        text="Aplicaciones",
        font=("Arial", 13),
        bg="#181818",
        fg="#aaaaaa"
    ).pack(
        pady=5
    )

    def menu_button(
        text,
        command
    ):

        tk.Button(
            menu,
            text=text,
            font=("Arial", 14),
            width=22,
            height=2,
            command=lambda: [
                menu.destroy(),
                command()
            ]
        ).pack(
            pady=5
        )

    menu_button(
        "🧮 Calculadora",
        open_calculator
    )

    menu_button(
        "📝 Notas",
        open_notes
    )

    menu_button(
        "📁 Archivos",
        open_files
    )

    menu_button(
        "👤 Perfil",
        open_profile
    )

    menu_button(
        "⚙️ Configuración",
        open_settings
    )

    menu_button(
        "🎮 Juegos",
        open_games
    )

    tk.Button(
        menu,
        text="⏻ Apagar WOLF OS",
        font=("Arial", 12, "bold"),
        command=lambda: [
            menu.destroy(),
            root.destroy()
        ]
    ).pack(
        pady=25
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
# APP BUTTONS
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

    tk.Button(
        apps,
        text=text,
        font=("Arial", 14),
        width=13,
        height=4,
        command=command
    ).grid(
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
    font=("Arial", 12, "bold"),
    command=open_start_menu
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
import tkinter as tk
from datetime import datetime
import os
import shutil

# ============================================================
# WOLF OS
# ============================================================

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))

NOTE_FILE = os.path.join(
    PROJECT_FOLDER,
    "wolf_note.txt"
)

TRASH_FOLDER = os.path.join(
    PROJECT_FOLDER,
    "Trash"
)

os.makedirs(TRASH_FOLDER, exist_ok=True)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("🐺 WOLF OS")

# FULLSCREEN
root.attributes("-fullscreen", True)


def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)


root.bind("<Escape>", exit_fullscreen)


# ============================================================
# DESKTOP
# ============================================================

desktop = tk.Frame(
    root,
    bg="#111111"
)

desktop.pack(
    expand=True,
    fill="both"
)


# ============================================================
# TOP BAR
# ============================================================

top_bar = tk.Frame(
    desktop,
    bg="#202020",
    height=55
)

top_bar.pack(
    side="top",
    fill="x"
)


tk.Label(
    top_bar,
    text="🐺 WOLF OS",
    font=("Arial", 20, "bold"),
    bg="#202020",
    fg="white"
).pack(
    side="left",
    padx=20
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
    padx=20
)


def update_clock():

    clock.config(
        text=datetime.now().strftime(
            "%H:%M:%S"
        )
    )

    root.after(
        1000,
        update_clock
    )


update_clock()


# ============================================================
# CALCULATOR
# ============================================================

def open_calculator():

    window = tk.Toplevel(root)

    window.title("🧮 Calculadora")

    window.geometry("400x550")

    display = tk.Entry(
        window,
        font=("Arial", 25),
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

        frame = tk.Frame(
            window
        )

        frame.pack(
            expand=True,
            fill="both"
        )

        for button in row:

            tk.Button(
                frame,
                text=button,
                font=("Arial", 18),
                command=lambda x=button: press(x)
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

    window = tk.Toplevel(root)

    window.title("📝 WOLF Notes")

    window.geometry("800x600")

    text = tk.Text(
        window,
        font=("Arial", 16),
        wrap="word",
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

            print(error)

    status = tk.Label(
        window,
        text="Escribe una nota."
    )

    status.pack(
        side="left",
        padx=10
    )

    def save():

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

                file.write(
                    content
                )

            status.config(
                text="✅ GUARDADO"
            )

        except Exception as error:

            status.config(
                text="❌ ERROR"
            )

            print(error)

    tk.Button(
        window,
        text="💾 GUARDAR",
        font=("Arial", 13, "bold"),
        command=save
    ).pack(
        side="right",
        padx=10,
        pady=10
    )

    text.focus_set()


# ============================================================
# TEXT FILE EDITOR
# ============================================================

def open_text_file(path):

    window = tk.Toplevel(root)

    window.title(
        "📝 " + os.path.basename(path)
    )

    window.geometry(
        "800x600"
    )

    text = tk.Text(
        window,
        font=("Arial", 15),
        wrap="word",
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

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            text.insert(
                "1.0",
                file.read()
            )

    except Exception as error:

        print(error)

    def save():

        try:

            content = text.get(
                "1.0",
                "end-1c"
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    content
                )

        except Exception as error:

            print(error)

    tk.Button(
        window,
        text="💾 GUARDAR",
        font=("Arial", 13, "bold"),
        command=save
    ).pack(
        side="right",
        padx=10,
        pady=10
    )

    text.focus_set()


# ============================================================
# TRASH
# ============================================================

def open_trash():

    window = tk.Toplevel(root)

    window.title("🗑️ WOLF Trash")

    window.geometry("700x550")

    tk.Label(
        window,
        text="🗑️ WOLF TRASH",
        font=("Arial", 26, "bold")
    ).pack(
        pady=20
    )

    file_list = tk.Listbox(
        window,
        font=("Arial", 15)
    )

    file_list.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=10
    )

    def refresh():

        file_list.delete(
            0,
            tk.END
        )

        items = os.listdir(
            TRASH_FOLDER
        )

        if not items:

            file_list.insert(
                tk.END,
                "🗑️ La papelera está vacía"
            )

        else:

            for item in sorted(items):

                path = os.path.join(
                    TRASH_FOLDER,
                    item
                )

                if os.path.isdir(path):

                    file_list.insert(
                        tk.END,
                        "📁 " + item
                    )

                else:

                    file_list.insert(
                        tk.END,
                        "📄 " + item
                    )

    def restore():

        selected = file_list.curselection()

        if not selected:
            return

        displayed = file_list.get(
            selected[0]
        )

        if displayed.startswith("🗑️"):
            return

        name = displayed[2:]

        source = os.path.join(
            TRASH_FOLDER,
            name
        )

        destination = os.path.join(
            PROJECT_FOLDER,
            name
        )

        if os.path.exists(destination):

            counter = 1

            while os.path.exists(destination):

                destination = os.path.join(
                    PROJECT_FOLDER,
                    f"{counter}_{name}"
                )

                counter += 1

        try:

            shutil.move(
                source,
                destination
            )

            refresh()

        except Exception as error:

            print(error)

    def delete_permanently():

        selected = file_list.curselection()

        if not selected:
            return

        displayed = file_list.get(
            selected[0]
        )

        if displayed.startswith("🗑️"):
            return

        name = displayed[2:]

        path = os.path.join(
            TRASH_FOLDER,
            name
        )

        try:

            if os.path.isdir(path):

                shutil.rmtree(path)

            else:

                os.remove(path)

            refresh()

        except Exception as error:

            print(error)

    def empty_trash():

        for item in os.listdir(
            TRASH_FOLDER
        ):

            path = os.path.join(
                TRASH_FOLDER,
                item
            )

            if os.path.isdir(path):

                shutil.rmtree(path)

            else:

                os.remove(path)

        refresh()

    buttons = tk.Frame(
        window
    )

    buttons.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Button(
        buttons,
        text="↩️ RESTAURAR",
        font=("Arial", 12, "bold"),
        command=restore
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        buttons,
        text="❌ ELIMINAR",
        font=("Arial", 12, "bold"),
        command=delete_permanently
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        buttons,
        text="🧹 VACIAR PAPELERA",
        font=("Arial", 12, "bold"),
        command=empty_trash
    ).pack(
        side="right",
        padx=5
    )

    refresh()


# ============================================================
# FILE EXPLORER
# ============================================================

def open_files():

    window = tk.Toplevel(root)

    window.title("📁 WOLF FILE EXPLORER")

    window.geometry("900x650")

    current_path = [
        PROJECT_FOLDER
    ]

    tk.Label(
        window,
        text="📁 WOLF FILE EXPLORER",
        font=("Arial", 25, "bold")
    ).pack(
        pady=15
    )

    path_label = tk.Label(
        window,
        anchor="w"
    )

    path_label.pack(
        fill="x",
        padx=15
    )

    toolbar = tk.Frame(
        window
    )

    toolbar.pack(
        fill="x",
        padx=10,
        pady=10
    )

    file_list = tk.Listbox(
        window,
        font=("Arial", 15)
    )

    file_list.pack(
        expand=True,
        fill="both",
        padx=15,
        pady=5
    )

    def refresh():

        file_list.delete(
            0,
            tk.END
        )

        path = current_path[0]

        path_label.config(
            text="📍 " + path
        )

        items = sorted(
            os.listdir(path)
        )

        for item in items:

            full_path = os.path.join(
                path,
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

    def home():

        current_path[0] = PROJECT_FOLDER

        refresh()

    def back():

        parent = os.path.dirname(
            current_path[0]
        )

        if parent.startswith(
            PROJECT_FOLDER
        ):

            current_path[0] = parent

            refresh()

    def new_folder():

        dialog = tk.Toplevel(
            window
        )

        dialog.title(
            "Nueva carpeta"
        )

        dialog.geometry(
            "400x220"
        )

        tk.Label(
            dialog,
            text="📁 NOMBRE",
            font=("Arial", 18, "bold")
        ).pack(
            pady=20
        )

        entry = tk.Entry(
            dialog,
            font=("Arial", 15)
        )

        entry.pack(
            padx=30,
            fill="x"
        )

        entry.focus_set()

        def create():

            name = entry.get().strip()

            if not name:
                return

            try:

                os.mkdir(
                    os.path.join(
                        current_path[0],
                        name
                    )
                )

                dialog.destroy()

                refresh()

            except Exception as error:

                print(error)

        tk.Button(
            dialog,
            text="CREAR",
            command=create
        ).pack(
            pady=20
        )

    def new_file():

        dialog = tk.Toplevel(
            window
        )

        dialog.title(
            "Nuevo archivo"
        )

        dialog.geometry(
            "400x220"
        )

        tk.Label(
            dialog,
            text="📄 NOMBRE",
            font=("Arial", 18, "bold")
        ).pack(
            pady=20
        )

        entry = tk.Entry(
            dialog,
            font=("Arial", 15)
        )

        entry.pack(
            padx=30,
            fill="x"
        )

        entry.focus_set()

        def create():

            name = entry.get().strip()

            if not name:
                return

            try:

                with open(
                    os.path.join(
                        current_path[0],
                        name
                    ),
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write("")

                dialog.destroy()

                refresh()

            except Exception as error:

                print(error)

        tk.Button(
            dialog,
            text="CREAR",
            command=create
        ).pack(
            pady=20
        )

    def move_to_trash():

        selected = file_list.curselection()

        if not selected:
            return

        displayed = file_list.get(
            selected[0]
        )

        name = displayed[2:]

        source = os.path.join(
            current_path[0],
            name
        )

        destination = os.path.join(
            TRASH_FOLDER,
            name
        )

        if os.path.exists(destination):

            counter = 1

            while os.path.exists(destination):

                destination = os.path.join(
                    TRASH_FOLDER,
                    f"{counter}_{name}"
                )

                counter += 1

        try:

            shutil.move(
                source,
                destination
            )

            refresh()

        except Exception as error:

            print(error)

    def open_item(event=None):

        selected = file_list.curselection()

        if not selected:
            return

        displayed = file_list.get(
            selected[0]
        )

        name = displayed[2:]

        path = os.path.join(
            current_path[0],
            name
        )

        if os.path.isdir(path):

            current_path[0] = path

            refresh()

        elif name.lower().endswith(
            (
                ".txt",
                ".py",
                ".json",
                ".md",
                ".csv"
            )
        ):

            open_text_file(
                path
            )

    tk.Button(
        toolbar,
        text="⬅️ ATRÁS",
        command=back
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        toolbar,
        text="🏠 INICIO",
        command=home
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        toolbar,
        text="🔄 ACTUALIZAR",
        command=refresh
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        toolbar,
        text="📁 NUEVA CARPETA",
        command=new_folder
    ).pack(
        side="right",
        padx=4
    )

    tk.Button(
        toolbar,
        text="📄 NUEVO ARCHIVO",
        command=new_file
    ).pack(
        side="right",
        padx=4
    )

    tk.Button(
        toolbar,
        text="🗑️ PAPELERA",
        command=move_to_trash
    ).pack(
        side="right",
        padx=4
    )

    file_list.bind(
        "<Double-Button-1>",
        open_item
    )

    refresh()


# ============================================================
# PROFILE
# ============================================================

def open_profile():

    window = tk.Toplevel(root)

    window.title("👤 Perfil")

    window.geometry("450x400")

    tk.Label(
        window,
        text="🐺",
        font=("Arial", 80)
    ).pack(
        pady=20
    )

    tk.Label(
        window,
        text="Agus",
        font=("Arial", 28, "bold")
    ).pack()

    tk.Label(
        window,
        text="Nivel 1\nXP: 0\nCoins: 0",
        font=("Arial", 16)
    ).pack(
        pady=20
    )


# ============================================================
# SETTINGS
# ============================================================

def open_settings():

    window = tk.Toplevel(root)

    window.title("⚙️ Configuración")

    window.geometry("500x400")

    tk.Label(
        window,
        text="⚙️ CONFIGURACIÓN",
        font=("Arial", 25, "bold")
    ).pack(
        pady=30
    )

    tk.Label(
        window,
        text="🐺 WOLF OS",
        font=("Arial", 16)
    ).pack()


# ============================================================
# GAMES
# ============================================================

def open_games():

    window = tk.Toplevel(root)

    window.title("🎮 WOLF GAME CENTER")

    window.geometry("600x450")

    tk.Label(
        window,
        text="🎮 WOLF GAME CENTER",
        font=("Arial", 28, "bold")
    ).pack(
        pady=40
    )

    tk.Label(
        window,
        text="Tus juegos aparecerán aquí.",
        font=("Arial", 16)
    ).pack()


# ============================================================
# START MENU
# ============================================================

def open_start_menu():

    menu = tk.Toplevel(root)

    menu.title("🐺 WOLF START")

    menu.geometry("400x650")

    menu.configure(
        bg="#181818"
    )

    tk.Label(
        menu,
        text="🐺 WOLF",
        font=("Arial", 35, "bold"),
        bg="#181818",
        fg="white"
    ).pack(
        pady=25
    )

    def add_button(
        text,
        command
    ):

        tk.Button(
            menu,
            text=text,
            font=("Arial", 14),
            width=25,
            height=2,
            command=lambda: [
                menu.destroy(),
                command()
            ]
        ).pack(
            pady=5
        )

    add_button(
        "🧮 Calculadora",
        open_calculator
    )

    add_button(
        "📝 Notas",
        open_notes
    )

    add_button(
        "📁 Archivos",
        open_files
    )

    add_button(
        "👤 Perfil",
        open_profile
    )

    add_button(
        "⚙️ Configuración",
        open_settings
    )

    add_button(
        "🎮 Juegos",
        open_games
    )

    add_button(
        "🗑️ Papelera",
        open_trash
    )

    tk.Button(
        menu,
        text="⏻ SALIR",
        font=("Arial", 13, "bold"),
        command=root.destroy
    ).pack(
        pady=25
    )


# ============================================================
# DESKTOP TITLE
# ============================================================

tk.Label(
    desktop,
    text="Bienvenido a WOLF OS",
    font=("Arial", 40, "bold"),
    bg="#111111",
    fg="white"
).pack(
    pady=70
)

tk.Label(
    desktop,
    text="Tu computadora. Tus reglas.",
    font=("Arial", 20),
    bg="#111111",
    fg="#aaaaaa"
).pack()


# ============================================================
# APP BUTTONS
# ============================================================

apps = tk.Frame(
    desktop,
    bg="#111111"
)

apps.pack(
    pady=40
)


def app_button(
    text,
    row,
    column,
    command
):

    tk.Button(
        apps,
        text=text,
        font=("Arial", 16),
        width=15,
        height=5,
        command=command
    ).grid(
        row=row,
        column=column,
        padx=12,
        pady=12
    )


app_button(
    "🧮\nCalculadora",
    0,
    0,
    open_calculator
)

app_button(
    "📝\nNotas",
    0,
    1,
    open_notes
)

app_button(
    "📁\nArchivos",
    0,
    2,
    open_files
)

app_button(
    "👤\nPerfil",
    1,
    0,
    open_profile
)

app_button(
    "⚙️\nConfiguración",
    1,
    1,
    open_settings
)

app_button(
    "🎮\nJuegos",
    1,
    2,
    open_games
)

app_button(
    "🗑️\nPapelera",
    2,
    0,
    open_trash
)


# ============================================================
# TASKBAR
# ============================================================

taskbar = tk.Frame(
    desktop,
    bg="#202020",
    height=70
)

taskbar.pack(
    side="bottom",
    fill="x"
)

tk.Button(
    taskbar,
    text="🐺 INICIO",
    font=("Arial", 14, "bold"),
    command=open_start_menu
).pack(
    side="left",
    padx=15,
    pady=12
)

tk.Button(
    taskbar,
    text="⏻ SALIR",
    font=("Arial", 14),
    command=root.destroy
).pack(
    side="right",
    padx=15,
    pady=12
)


# ============================================================
# START WOLF OS
# ============================================================

root.mainloop()

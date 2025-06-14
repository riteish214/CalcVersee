import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"

        self.themes = {
            "light": {
                "bg": "#f7f7f7",
                "fg": "#2e2e2e",
                "button_bg": "#e6e6e6",
                "button_fg": "#2e2e2e",
                "entry_bg": "#ffffff",
                "entry_fg": "#2e2e2e",
                "highlight_bg": "#b0c4de",
                "highlight_fg": "#000000",
                "treeview_bg": "#ffffff",
                "treeview_fg": "#2e2e2e",
                "warning": "#d9ad00",
                "error": "#d9534f",
                "success": "#5cb85c"
            },
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#f2f2f2",
                "button_bg": "#2e2e2e",
                "button_fg": "#f2f2f2",
                "entry_bg": "#121212",   # darker entry background
                "entry_fg": "#ffffff",   # bright white text
                "highlight_bg": "#5a6475",
                "highlight_fg": "#ffffff",
                "treeview_bg": "#2a2a2a",
                "treeview_fg": "#f2f2f2",
                "warning": "#c49a00",
                "error": "#d94f4f",
                "success": "#4caf50"
            }
        }

        self.style = ttk.Style()
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name):
        if theme_name not in self.themes:
            return

        theme = self.themes[theme_name]
        self.current_theme = theme_name
        self.root.configure(bg=theme["bg"])

        self.style.theme_use("default")
        self.style.configure(".", background=theme["bg"], foreground=theme["fg"], font=("Segoe UI", 10))
        self.style.configure("TFrame", background=theme["bg"])
        self.style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
        self.style.configure("TButton", background=theme["button_bg"], foreground=theme["button_fg"])
        self.style.map("TButton",
            background=[("active", theme["highlight_bg"])],
            foreground=[("active", theme["highlight_fg"])])

        self.style.configure("TEntry",
            fieldbackground=theme["entry_bg"],
            foreground=theme["entry_fg"],
            insertcolor=theme["entry_fg"])  # caret color

        self.style.configure("Treeview", background=theme["treeview_bg"],
                             fieldbackground=theme["treeview_bg"], foreground=theme["treeview_fg"])
        self.style.map("Treeview",
            background=[("selected", theme["highlight_bg"])],
            foreground=[("selected", theme["highlight_fg"])])

        self.style.configure("TNotebook", background=theme["bg"])
        self.style.configure("TNotebook.Tab",
            background=theme["button_bg"],
            foreground=theme["fg"],
            font=("Segoe UI", 10, "bold"),
            padding=[10, 5])
        self.style.map("TNotebook.Tab",
            background=[("selected", theme["highlight_bg"]), ("active", theme["button_bg"])],
            foreground=[("selected", theme["highlight_fg"]), ("active", theme["fg"])])

        # Fix Treeview selection map
        fixed_map = lambda opt: [elm for elm in self.style.map("Treeview", query_opt=opt)
                                 if elm[:2] != ("!disabled", "!selected")]
        self.style.map("Treeview",
            foreground=fixed_map("foreground"),
            background=fixed_map("background"))

    def toggle_theme(self):
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)


def create_app():
    root = tk.Tk()
    root.title("Themed UI with Entry Fix")
    root.geometry("600x400")

    theme_manager = ThemeManager(root)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_names = ["Basic", "Scientific", "Equation Solver", "Matrix", "Programmer", "Unit Converter", "Currency", "Graph", "History"]

    for name in tab_names:
        frame = ttk.Frame(notebook)
        label = ttk.Label(frame, text=f"This is the {name} tab")
        label.pack(pady=10)
        
        # Entry box for testing visibility
        entry = ttk.Entry(frame, width=20)
        entry.insert(0, "36")
        entry.pack(pady=10)

        notebook.add(frame, text=name)

    toggle_btn = ttk.Button(root, text="Toggle Theme", command=theme_manager.toggle_theme)
    toggle_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_app()

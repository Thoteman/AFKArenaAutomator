import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from src.theme_manager import ThemeManager

class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoAFK")

        self.theme_manager = ThemeManager(root)
        self.theme_manager.apply_theme(self.theme_manager.theme)

        self.create_menu()
        self.build_layout()

    def create_menu(self):
        menu_bar = tb.Menu(self.root)

        # File menu
        file_menu = tb.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View menu from ThemeManager
        view_menu = self.theme_manager.create_view_menu(menu_bar)
        menu_bar.add_cascade(label="View", menu=view_menu)

        # Help menu
        help_menu = tb.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def build_layout(self):
        frame = tb.Frame(self.root)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Left Panel (Buttons)
        left_panel = tb.Frame(frame)
        left_panel.pack(side=LEFT, fill=Y, padx=10)

        btn_texts = ["Start Dailies", "Task 2", "Task 3", "Task 4", "Task 5"]
        for text in btn_texts:
            tb.Button(left_panel, text=text, bootstyle=PRIMARY, width=20).pack(pady=5)

        # Right Panel (Output)
        right_panel = tb.Frame(frame)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        self.output = tb.ScrolledText(right_panel, wrap="word", height=25)
        self.output.pack(fill=BOTH, expand=True)
        self.output.config(state="disabled")
        self.log("Welcome to AFK Arena Bot!")

    def show_settings(self):
        messagebox.showinfo("Settings", "Settings dialog would appear here.")

    def show_help(self):
        messagebox.showinfo("Help", "Help info goes here.")

    def show_about(self):
        messagebox.showinfo("About", "AFK Arena Bot\nVersion 1.0")

    def log(self, message):
        self.output.config(state="normal")
        self.output.insert("end", message + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

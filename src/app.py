# src/app.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from src.config_manager import ConfigManager
from src.settings_window import SettingsWindow

class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoAFK")
        self.config_manager = ConfigManager()

        # Apply the theme directly
        self.config_manager.apply_theme(self.root)

        # Tasks
        self.task_vars = {
            task: tb.BooleanVar(value=val)
            for task, val in self.config_manager.load_tasks().items()
        }

        self.create_menu()
        self.build_layout()

    def create_menu(self):
        menu_bar = tb.Menu(self.root)

        # File
        file_menu = tb.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Settings", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View
        view_menu = self.config_manager.create_view_menu(menu_bar, self.root)
        menu_bar.add_cascade(label="View", menu=view_menu)

        # Help
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
        SettingsWindow(self.root, self.config_manager, self.task_vars)

    def show_help(self):
        messagebox.showinfo("Help", "Help info goes here.")

    def show_about(self):
        messagebox.showinfo("About", "AFK Arena Bot\nVersion 1.0")

    def log(self, message):
        self.output.config(state="normal")
        self.output.insert("end", message + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def save_task_settings(self):
        self.config_manager.save_tasks({task: var.get() for task, var in self.task_vars.items()})
# src/settings_window.py
import ttkbootstrap as tb
from tkinter import Toplevel, BooleanVar
from src.config_manager import ConfigManager

class SettingsWindow:
    def __init__(self, master, config: ConfigManager, task_vars: dict):
        self.top = Toplevel(master)
        self.top.title("Settings")
        self.config = config
        self.task_vars = task_vars

        self.check_vars = {}
        self.build_ui()
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        frame = tb.Frame(self.top, padding=10)
        frame.pack(fill="both", expand=True)

        for task, var in self.task_vars.items():
            check = tb.Checkbutton(
                frame, text=task, variable=var, bootstyle="success-round-toggle"
            )
            check.pack(anchor="w", pady=5)

    def on_close(self):
        task_values = {task: var.get() for task, var in self.task_vars.items()}
        self.config.save_tasks(task_values)
        self.top.destroy()


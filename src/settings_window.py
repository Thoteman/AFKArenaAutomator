# src/settings_window.py
import ttkbootstrap as tb
from tkinter import Toplevel, BooleanVar
from src.config_manager import ConfigManager

class SettingsWindow:
    def __init__(self, master, config: ConfigManager, task_vars: dict, logger):
        self.top = Toplevel(master)
        self.top.title("Settings")
        self.config = config
        self.task_vars = task_vars
        self.logger = logger

        self.check_vars = {}
        self.build_ui()
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        frame = tb.Frame(self.top, padding=10)
        frame.pack(fill="both", expand=True)

        for task, var in self.task_vars.items():
            row = tb.Frame(frame)
            row.pack(anchor="w", pady=5, fill="x")

            if isinstance(var, BooleanVar):
                check = tb.Checkbutton(
                    row, text=task, variable=var, bootstyle="success-round-toggle"
                )
                check.pack(anchor="w")
            else:
                tb.Label(row, text=task).pack(side="left", padx=(0, 5))
                entry = tb.Entry(row, textvariable=var, width=5)
                entry.pack(side="left")

                # Optional input validation (allow only integers)
                def validate(P): return P.isdigit() or P == ""
                vcmd = (self.top.register(validate), '%P')
                entry.config(validate="key", validatecommand=vcmd)

    def on_close(self):
        task_values = {task: var.get() for task, var in self.task_vars.items()}
        self.config.save_tasks(task_values)
        self.logger("Settings saved!", "success")
        self.top.destroy()


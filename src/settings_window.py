# src/settings_window.py
import ttkbootstrap as tb
from tkinter import Toplevel, BooleanVar
from src.config_manager import ConfigManager, global_defaults

class SettingsWindow:
    def __init__(self, master, config: ConfigManager, task_vars: dict, logger):
        self.top = Toplevel(master)
        self.top.title("Settings")
        self.config = config
        self.original_task_vars = task_vars
        self.logger = logger

        self.task_vars = {
            key: (tb.BooleanVar(value=var.get()) if isinstance(var, tb.BooleanVar)
                  else tb.IntVar(value=var.get()))
            for key, var in task_vars.items()
        }

        self.build_ui()
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        frame = tb.Frame(self.top, padding=10)
        frame.pack(fill="both", expand=True)

        # Define task categories and their tasks
        categories = {
            "Global Settings": [
                "Test Server",
                "Max Attempts",
                "Delay",
            ],
            "Campaign Tasks": [
                "Claim AFK Rewards",
                "Campaign Battle",
                "Claim Fast Rewards",
                "Amount of Fast Rewards",
                "Friendship Points",
                "Loan Mercenaries",
                "Read Mail",
                "Delete Mail",
            ],
            "Dark Forest Tasks": [
                "Bounty Board",
                "Temporal Rift Fountain",
                "King's Tower Battle",
                "Arcane Labyrinth",
                "Treasure Scramble",
                "Arena of Heroes",
                "Amount of Arena Battles",
                "Gladiator Coins",
            ],
            "Ranhorn Tasks": [
                "Store Purchases",
                "Use quick buy",
                "Use refresh",
                "Noble Tavern",
                "Temple of Ascension",
                "Resonating Crystal",
                "Oak Inn Gifts",
                "Draconis gifts",
                "Guid hunt",
                "Twisted Realm",
            ],
            "Banner Tasks": [
                "Claim bags",
                "Claim quests",
                "Claim free merchants",
                "Event markers",
            ],
        }

        for i, (category, tasks) in enumerate(categories.items()):
            col = tb.LabelFrame(frame, text=category, padding=10)
            col.grid(row=0, column=i, padx=10, pady=5, sticky="n")

            for task in tasks:
                var = self.task_vars[task]
                if isinstance(var, tb.BooleanVar):
                    tb.Checkbutton(
                        col, text=task, variable=var, bootstyle="success-round-toggle"
                    ).pack(anchor="w", pady=2)
                else:
                    tb.Label(col, text=task).pack(anchor="w", pady=(5, 0))
                    tb.Entry(col, textvariable=var, width=5).pack(anchor="w", pady=(0, 5))
        
        button_frame = tb.Frame(self.top)
        button_frame.pack(fill="x", pady=(0, 10), padx=10)
        
        tb.Button(
            button_frame,
            text="Save",
            bootstyle="success",
            command=self.save_settings
        ).pack(side="right")

    def save_settings(self):
        task_values = {}
        global_values = {}
        for task, var in self.task_vars.items():
            val = var.get()

            if task in global_defaults:
                global_values[task] = val
            else:
                task_values[task] = val

            self.original_task_vars[task].set(val)

        self.config.save_globals(global_values)
        self.config.save_tasks(task_values)

        self.logger("Settings saved!", "success")
        self.top.destroy()


    def on_close(self):
        self.top.destroy()


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

        # Define task categories and their tasks
        categories = {
            "Campaign Tasks": [
                "Claim AFK Rewards",
                "Campaign Battle",
                "Claim Fast Rewards",
                "Amount of Fast Rewards",
            ],
            "Dark Forest Tasks": [
                "Bounty Board",
                "Temporal Rift Fountain",
                "King's Tower Battle",
                "Arcane Labyrinth",
                "Treasure Scramble",
                "Arena of Heroes",
                "Amount of Arena Battles",
                "Legends Challenger Coins",
                "Legends Championship Betting",
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
                "Solemn vow",
                "Friendship points",
                "Read mail",
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


    def on_close(self):
        task_values = {task: var.get() for task, var in self.task_vars.items()}
        self.config.save_tasks(task_values)
        self.logger("Settings saved!", "success")
        self.top.destroy()


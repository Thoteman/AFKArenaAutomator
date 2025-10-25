# src/settings_window.py
from numpy import var
import ttkbootstrap as tb
from tkinter import Toplevel, BooleanVar
from src.config_manager import ConfigManager, global_defaults
from src.strings import combobox_awakened, combobox_celepog, combobox_4f

class SettingsWindow:
    def __init__(self, master, config: ConfigManager, task_vars: dict, logger):
        self.top = Toplevel(master)
        self.top.title("Settings")
        self.config = config
        self.original_task_vars = task_vars
        self.logger = logger

        self.task_vars = {}
        for key, var in task_vars.items():
            try:
                value = var.get()
            except Exception:
                value = var

            if isinstance(var, tb.BooleanVar):
                self.task_vars[key] = tb.BooleanVar(value=value)
            elif isinstance(var, tb.StringVar):
                self.task_vars[key] = tb.StringVar(value=value)
            elif isinstance(var, str):
                self.task_vars[key] = tb.StringVar(value=value)
            elif isinstance(var, tb.IntVar):
                self.task_vars[key] = tb.IntVar(value=value)

        self.build_ui()
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

        # Make the window modal
        self.top.transient(master)
        self.top.grab_set()
        self.top.focus()

    def build_ui(self):
        frame = tb.Frame(self.top, padding=10)
        frame.pack(fill="both", expand=True)

        # Define task categories and their tasks
        categories = {
            "Global Settings": [
                "Emulator Port",
                "Test Server",
                "Max Attempts",
                "Delay",
            ],
            "Auto Push Settings": [
                "Copy Artifacts",
                "Copy Singlestage Formations",
                "Copy Formation #",
            ],
            "Campaign Tasks": [
                "Claim AFK Rewards",
                "Campaign Battle",
                "Claim Fast Rewards",
                "Amount of Fast Rewards",
            ],
            "Dark Forest Tasks": [
                "Bounty Board",
                "Claim 10 weekly Staves (GG)",
                "Treasure Scramble",
                "Arena of Heroes",
                "Amount of Arena Battles",
                "Claim Gladiator Coins",
                "Temporal Rift Fountain",
                "King's Tower Battle",
                "Arcane Labyrinth",
            ],
            "Ranhorn Tasks": [
                "Store Purchases",
                "Amount of Refreshes",
                "Hunting Contract",
                "Guild hunt",
                "Twisted Realm",
                "Oak Inn Gifts",
                # "Draconis gifts",
            ],
            "Misc Tasks": [
                "Friendship Points",
                "Loan Mercenaries",
                "Read Mail",
                "Delete Mail",
                # "Claim quests",
                # "Claim free merchants",
            ],
            ## TODO: turn this on next time this event comes around
            # "Unlimited Summons": [
            #     "Awakened",
            #     "Awakened 2 (optional)",
            #     "Awakened 3 (optional)",
            #     "Celepog",
            #     "Celepog 2 (optional)",
            #     "Celepog 3 (optional)",
            #     "4F",
            #     "4F 2 (optional)",
            #     "4F 3 (optional)",
            #     "4F 4 (optional)",
            #     "4F 5 (optional)",
            #     "Overwrite on success",
            #     "Double 4F",
            # ],
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
                elif task.startswith("Awakened"):
                    tb.Label(col, text=task).pack(anchor="w", pady=(5, 0))
                    tb.Combobox(col, value=combobox_awakened, textvariable=var, state='readonly').pack(anchor="w", pady=(0, 5))
                elif task.startswith("Celepog"):
                    tb.Label(col, text=task).pack(anchor="w", pady=(5, 0))
                    tb.Combobox(col, value=combobox_celepog, textvariable=var, state='readonly').pack(anchor="w", pady=(0, 5))
                elif task.startswith("4F"):
                    tb.Label(col, text=task).pack(anchor="w", pady=(5, 0))
                    tb.Combobox(col, value=combobox_4f, textvariable=var, state='readonly').pack(anchor="w", pady=(0, 5))
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


# src/config_manager.py
import configparser
import ttkbootstrap as tb
import tkinter as tk
from src.utils import get_config_path

CONFIG_PATH = get_config_path()

global_defaults = {
    # global settings
    "Test Server": False,
    "Max Attempts": 3,
    "Delay": 3,
    # auto push tasks
    "Copy Artifacts": False,
    "Copy Singlestage Formations": False,
    "Copy Formation #": 1,
}

task_defaults = {
    # campaign tasks
    "Claim AFK Rewards": True,
    "Campaign Battle": True,
    "Claim Fast Rewards": True,
    "Amount of Fast Rewards": 1,
    # dark forest tasks
    "Bounty Board": True,
    "Claim 10 weekly Staves (GG)": False,
    "Treasure Scramble": True,
    "Arena of Heroes": True,
    "Amount of Arena Battles": 3,
    "Claim Gladiator Coins": True,
    "Temporal Rift Fountain": True,
    "King's Tower Battle": True,
    "Arcane Labyrinth": True,
    # ranhorn tasks
    "Wall of Legends": True,
    "Store Purchases": False,
    "Amount of Refreshes": 3,
    "Resonating Crystal": False,
    "Hunting Contract": False,
    "Guild hunt": False,
    "Twisted Realm": False,
    "Oak Inn Gifts": False,
    "Draconis gifts": False,
    # misc tasks
    "Friendship Points": True,
    "Loan Mercenaries": False,
    "Read Mail": True,
    "Delete Mail": False,
    "Claim bags": False,
    "Claim quests": False,
    "Claim free merchants": False,
    "Event markers": False,
    # unlimited summons
    "Awakened": "aTalene",
    "Awakened 2 (optional)": "aTalene",
    "Awakened 3 (optional)": "aTalene",
    "Celepog": "Athalia",
    "Celepog 2 (optional)": "Athalia",
    "Celepog 3 (optional)": "Athalia",
}

class ConfigManager:
    def __init__(self, path=CONFIG_PATH):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path)

        self.theme = self.load_theme()
        self.light_mode_var = tk.BooleanVar(value=(self.theme == "pulse"))
        self.dark_mode_var = tk.BooleanVar(value=(self.theme == "cyborg"))

    def apply_theme(self, app_window):
        app_window.style.theme_use(self.theme)

    def create_view_menu(self, parent_menu, app_window):
        view_menu = tb.Menu(parent_menu, tearoff=0)
        view_menu.add_checkbutton(
            label="Light Mode",
            command=lambda: self.change_theme("pulse", app_window),
            variable=self.light_mode_var
        )
        view_menu.add_checkbutton(
            label="Dark Mode",
            command=lambda: self.change_theme("cyborg", app_window),
            variable=self.dark_mode_var
        )
        return view_menu


    def change_theme(self, theme_name, app_window=None):
        if theme_name == self.theme:
            return
        self.theme = theme_name
        if app_window:
            self.apply_theme(app_window)
        self.save_theme(theme_name)

        self.light_mode_var.set(theme_name == "pulse")
        self.dark_mode_var.set(theme_name == "cyborg")


    def load_theme(self):
        return self.config.get("Appearance", "theme", fallback="cyborg")

    def save_theme(self, theme):
        if "Appearance" not in self.config:
            self.config["Appearance"] = {}
        self.config["Appearance"]["theme"] = theme
        self._write()

    def load_tasks(self):
        if "Tasks" not in self.config:
            self.config["Tasks"] = {}
        return {
            task: (
                self.config.getboolean("Tasks", task, fallback=default)
                if isinstance(default, bool)
                else self.config.get("Tasks", task, fallback=default)
                if isinstance(default, str)
                else self.config.getint("Tasks", task, fallback=default)
            )
            for task, default in task_defaults.items()
        }

    def save_tasks(self, task_values):
        if "Tasks" not in self.config:
            self.config["Tasks"] = {}
        for task, val in task_values.items():
            self.config["Tasks"][task] = str(val)
        self._write()

    def load_globals(self):
        if "Global" not in self.config:
            self.config["Global"] = {}
        return {
            key: (
                self.config.getboolean("Global", key, fallback=default)
                if isinstance(default, bool)
                else self.config.getint("Global", key, fallback=default)
            )
            for key, default in global_defaults.items()
        }

    def save_globals(self, global_values):
        if "Global" not in self.config:
            self.config["Global"] = {}
        for key, val in global_values.items():
            self.config["Global"][key] = str(val)
        self._write()


    def _write(self):
        with open(self.path, "w") as configfile:
            self.config.write(configfile)

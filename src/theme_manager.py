import tkinter as tk
import ttkbootstrap as tb
import configparser
import os
from src.utils import get_config_path

CONFIG_PATH = get_config_path()

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.config = configparser.ConfigParser()
        self.theme = self.load_theme()

        self.theme_var = tk.StringVar(value=self.theme)


    def create_view_menu(self, parent_menu):
        view_menu = tb.Menu(parent_menu, tearoff=0)
        view_menu.add_radiobutton(label="Light Mode", 
                                value="pulse", 
                                variable=self.theme_var,
                                command=lambda: self.change_theme("pulse"))
        view_menu.add_radiobutton(label="Dark Mode", 
                                value="cyborg", 
                                variable=self.theme_var,
                                command=lambda: self.change_theme("cyborg"))
        return view_menu


    def change_theme(self, theme_name):
        if theme_name == self.theme:
            return
        self.theme = theme_name
        self.apply_theme(theme_name)
        self.save_theme(theme_name)

        self.light_mode_var.set(theme_name == "pulse")
        self.dark_mode_var.set(theme_name == "cyborg")

    def apply_theme(self, theme_name):
        self.root.style.theme_use(theme_name)

    def load_theme(self):
        if not os.path.exists(CONFIG_PATH):
            return "cyborg"  # default
        self.config.read(CONFIG_PATH)
        return self.config.get("Appearance", "theme", fallback="cyborg")

    def save_theme(self, theme_name):
        if "Appearance" not in self.config:
            self.config["Appearance"] = {}
        self.config["Appearance"]["theme"] = theme_name
        with open(CONFIG_PATH, "w") as configfile:
            self.config.write(configfile)
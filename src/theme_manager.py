import tkinter as tk
import ttkbootstrap as tb
import configparser
import os

CONFIG_PATH = "config.ini"

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.config = configparser.ConfigParser()
        self.theme = self.load_theme()

        self.light_mode_var = tk.BooleanVar(value=(self.theme == "pulse"))
        self.dark_mode_var = tk.BooleanVar(value=(self.theme == "cyborg"))

    def create_view_menu(self, parent_menu):
        view_menu = tb.Menu(parent_menu, tearoff=0)
        view_menu.add_checkbutton(label="Light Mode",
                                  command=lambda: self.change_theme("pulse"),
                                  variable=self.light_mode_var)
        view_menu.add_checkbutton(label="Dark Mode",
                                  command=lambda: self.change_theme("cyborg"),
                                  variable=self.dark_mode_var)
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
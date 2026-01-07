# src/app.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from ttkbootstrap.scrolled import ScrolledText
from tkinter import messagebox
from datetime import datetime
from importlib import resources
import threading
from src.config_manager import ConfigManager
from src.settings_window import SettingsWindow
from src.autoafk import take_screenshot, start_daily_tasks, auto_push_campaign, auto_push_tower, auto_push_lb, auto_push_m, auto_push_w, auto_push_gb, auto_push_cel, auto_push_hypo, stop_action, unlimited_summons, illusory_journey, disable_buttons

class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AFK Arena Automator")
        self.config_manager = ConfigManager()

        # Apply the theme directly
        self.config_manager.apply_theme(self.root)

        # Tasks
        globals = self.config_manager.load_globals()
        tasks = self.config_manager.load_tasks()

        self.task_vars = {
            task: (tb.BooleanVar(value=val) if isinstance(val, bool) else tb.StringVar(value=val) if isinstance(val, str) else tb.IntVar(value=val))
            for task, val in {**globals, **tasks}.items()
        }

        self.buttons = {}

        self.create_menu()
        self.build_layout()
        # self.sanity_check_adbauto()

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

    def show_settings(self):
        SettingsWindow(self.root, self.config_manager, self.task_vars, self.log)

    def show_help(self):
        messagebox.showinfo("Help", "Help info goes here.")

    def show_about(self):
        messagebox.showinfo("About", "AFK Arena Automator\nVersion 0.3.0 Beta\nDeveloped by Thoteman")

    def build_layout(self):
        frame = tb.Frame(self.root)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Left Panel (Buttons)
        left_panel = tb.Frame(frame)
        left_panel.pack(side=LEFT, fill=Y, padx=10)

        # Button Functions
        button_actions = {
            "Settings": self.show_settings,
            "Daily tasks": lambda: threading.Thread(target=start_daily_tasks, args=(self.log,), daemon=True).start(),
            "Push Campaign": lambda: threading.Thread(target=auto_push_campaign, args=(self.log,), daemon=True).start(),
            "Push Kings Tower": lambda: threading.Thread(target=auto_push_tower, args=(self.log,), daemon=True).start(),
            "Push Tower of Light": lambda: threading.Thread(target=auto_push_lb, args=(self.log,), daemon=True).start(),
            "Push Brutal Citadel": lambda: threading.Thread(target=auto_push_m, args=(self.log,), daemon=True).start(),
            "Push World Tree": lambda: threading.Thread(target=auto_push_w, args=(self.log,), daemon=True).start(),
            "Push Forsaken Necropolis": lambda: threading.Thread(target=auto_push_gb, args=(self.log,), daemon=True).start(),
            "Push Celestial Sanctum": lambda: threading.Thread(target=auto_push_cel, args=(self.log,), daemon=True).start(),
            "Push Infernal Fortress": lambda: threading.Thread(target=auto_push_hypo, args=(self.log,), daemon=True).start(),
            # "Screenshot": lambda: threading.Thread(target=take_screenshot, args=(self.log,), daemon=True).start(),
            "Unlimited Summons": lambda: threading.Thread(target=unlimited_summons, args=(self.log,), daemon=True).start(),
            "Illusory Journey": lambda: threading.Thread(target=illusory_journey, args=(self.log,), daemon=True).start(),
            "Stop Current Action": lambda: threading.Thread(target=stop_action, args=(self.log,), daemon=True).start(),
        }

        btn_texts = button_actions.keys()
        for text in btn_texts:
            pady = (5, 25) if text == "Settings" or text == "Daily tasks" or text == "Push Infernal Fortress" or text == "Illusory Journey" else 5
            state = "normal" if text != "Unlimited Summons" else "disabled" ##TODO: This is how to activate and deactivate buttons!
            style = PRIMARY if text != "Stop Current Action" else DANGER
            btn = tb.Button(left_panel, text=text, bootstyle=style, width=25, command=button_actions[text], state=state)
            btn.pack(pady=pady)
            self.buttons[text] = btn

        disable_buttons(self.buttons)

        # Right Panel (Output)
        right_panel = tb.Frame(frame)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        self.output = ScrolledText(right_panel, wrap="word", height=25)
        self.output.pack(fill=BOTH, expand=True)
        self.output.text.configure(state="disabled")
        self.log("Welcome to AFK Arena Automator!\nDeveloped by Thoteman from 10,000 Diamonds\nJoin our Discord Server: bit.ly/afk10kd\nJoin the Floofpire Discord for support\n\n", "info", True)
        self.log("DISCLAIMER:\nThis bot is still in development! This is a beta release! Not everything is working yet!\nI released this version already for testing / auto pushing towers / auto pushing campaign!\n\n", "error", True)
                                                                              

    def log(self, message, level="info", no_timestamp=False):
        def _log():
            style = Style()
            color_map = {
                "info": style.colors.get("info"),
                "success": style.colors.get("success"),
                "warning": style.colors.get("warning"),
                "error": style.colors.get("danger"),
            }

            color = color_map.get(level, style.colors.get("secondary"))
            if no_timestamp:
                full_message = f"{message}" if message else ""
            else:
                timestamp = datetime.now().strftime("[%H:%M:%S]")  # Add timestamp
                full_message = f"{timestamp} {message}" if message else ""

            self.output.text.configure(state="normal")
            self.output.text.insert("end", full_message + "\n", level)
            self.output.text.tag_config(level, foreground=color)
            self.output.text.see("end")
            self.output.text.configure(state="disabled")
        self.output.after(0, _log)


    def save_task_settings(self):
        self.config_manager.save_tasks({task: var.get() for task, var in self.task_vars.items()})

    ## TODO: Remove this function after beta testing
    def sanity_check_adbauto(self):
        try:
            adb_path = resources.files("adbauto").joinpath("bin/adb.exe")
            scrcpy_path = resources.files("adbauto").joinpath("scrcpy/scrcpy-server.jar")

            self.log(f"[Sanity Check] adb.exe exists: {adb_path.exists()}", "info")
            self.log(f"[Sanity Check] scrcpy-server.jar exists: {scrcpy_path.exists()}", "info")
            self.log(f"[Sanity Check] adb.exe path: {adb_path}", "info")
            self.log(f"[Sanity Check] scrcpy-server path: {scrcpy_path}", "info")

        except Exception as e:
            self.log(f"[Sanity Check ERROR] {e}", "error")
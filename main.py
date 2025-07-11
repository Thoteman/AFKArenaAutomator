import ttkbootstrap as tb
from src.app import BotApp
from src.utils import resource_path

### Monkey ptching for flashing consoles ###
import subprocess
import sys

# Only apply on Windows
if sys.platform == "win32":
    original_popen = subprocess.Popen
    original_run = subprocess.run

    # Configure STARTUPINFO to hide console windows
    hidden_si = subprocess.STARTUPINFO()
    hidden_si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Monkey patch Popen
    def hidden_popen(*args, **kwargs):
        if "startupinfo" not in kwargs:
            kwargs["startupinfo"] = hidden_si
        return original_popen(*args, **kwargs)

    # Monkey patch run
    def hidden_run(*args, **kwargs):
        if "startupinfo" not in kwargs:
            kwargs["startupinfo"] = hidden_si
        return original_run(*args, **kwargs)

    subprocess.Popen = hidden_popen
    subprocess.run = hidden_run
### End of monkey patching ###

if __name__ == "__main__":
    app = tb.Window(themename="cyborg")
    app.iconbitmap(resource_path("icon.ico"))
    app.app = BotApp(app)  # Attach BotApp to the root
    app.mainloop()
import ttkbootstrap as tb
from src.app import BotApp
from src.utils import resource_path
from importlib import resources

def sanity_check_adbauto():
    try:
        adb_path = resources.files("adbauto").joinpath("bin/adb.exe")
        scrcpy_path = resources.files("adbauto").joinpath("scrcpy/scrcpy-server.jar")

        print("[Sanity Check] adb.exe exists:", adb_path.exists())
        print("[Sanity Check] scrcpy-server.jar exists:", scrcpy_path.exists())
        print("[Sanity Check] adb.exe path:", adb_path)
        print("[Sanity Check] scrcpy-server path:", scrcpy_path)

    except Exception as e:
        print("[Sanity Check ERROR]", e)

if __name__ == "__main__":
    sanity_check_adbauto()

    app = tb.Window(themename="cyborg")
    app.iconbitmap(resource_path("icon.ico"))
    app.app = BotApp(app)  # Attach BotApp to the root
    app.mainloop()
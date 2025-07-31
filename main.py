import ttkbootstrap as tb
from src.app import BotApp
from src.utils import resource_path

if __name__ == "__main__":
    app = tb.Window(themename="cyborg")
    app.iconbitmap(resource_path("icon.ico"))
    app.app = BotApp(app)  # Attach BotApp to the root
    app.mainloop()
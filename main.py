import ttkbootstrap as tb
from src.app import BotApp

if __name__ == "__main__":
    app = tb.Window(themename="cyborg")
    app.app = BotApp(app)  # Attach BotApp to the root
    app.mainloop()
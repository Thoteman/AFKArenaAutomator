import ttkbootstrap as tb
from src.app import BotApp

if __name__ == "__main__":
    root = tb.Window(themename="cyborg")
    app = BotApp(root)
    root.mainloop()
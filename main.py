import tkinter as tk
from gui.gui_app import BotGui


def main():
    root = tk.Tk()
    app = BotGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
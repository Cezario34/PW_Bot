import pygetwindow as gw
import time


class GameWindow:
    """Класс для работы с окном игры"""

    def __init__(self, partial_title: str = "luk"):
        self.partial_title = partial_title
        self.win = None
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0

    def activate(self) -> bool:
        """Ищет и активирует окно игры"""
        windows = gw.getWindowsWithTitle(self.partial_title)

        if not windows:
            print(f"Окно с названием '{self.partial_title}' не найдено")
            return False

        self.win = windows[0]

        if self.win.isMinimized:
            self.win.restore()

        self.win.activate()
        time.sleep(0.4)

        # Обновляем координаты
        self.left = self.win.left
        self.top = self.win.top
        self.width = self.win.width
        self.height = self.win.height

        print(f"Окно активировано: {self.win.title}")
        return True

    def update_position(self):
        """Обновляет текущие координаты окна (на случай, если окно передвинули)"""
        if self.win:
            self.left = self.win.left
            self.top = self.win.top
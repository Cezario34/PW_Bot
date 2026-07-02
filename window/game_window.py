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

def is_game_active(partial_title="Avelon"):
    """
    Проверяет, активно ли окно игры в данный момент.
    Возвращает True, если окно в фокусе, иначе False.
    """
    try:
        active_window = gw.getActiveWindow()
        if active_window is None:
            return False

        # Проверяем, содержит ли заголовок активного окна название игры
        if partial_title.lower() in active_window.title.lower():
            return True
        else:
            return False
    except Exception:
        return False

if __name__ == "__main__":
    # Создаём объект окна (partial_title можно поменять)
    game = GameWindow(partial_title="Avelon Perfect World")   # или "Avelon", или часть имени окна

    print("Пытаемся активировать окно игры...")

    if game.activate():
        print("\n=== Окно успешно активировано ===")
        print(f"Заголовок окна : {game.win.title}")
        print(f"Позиция        : left={game.left}, top={game.top}")
        print(f"Размер         : width={game.width}, height={game.height}")
        print(f"Центр экрана   : X={game.left + game.width // 2}, Y={game.top + game.height // 2}")

        # Небольшая пауза, чтобы ты мог посмотреть
        time.sleep(5)
    else:
        print("Не удалось найти окно. Проверь partial_title.")
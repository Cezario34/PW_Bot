import pygetwindow as gw
import pyautogui
import time
import sys


def get_game_window(partial_title="luk"):
    print("[DEBUG] Ищу окно...")
    windows = gw.getWindowsWithTitle(partial_title)
    if not windows:
        print("[DEBUG] Окно не найдено!")
        return None
    win = windows[0]
    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(0.4)
    print(f"[DEBUG] Окно активировано: {win.title}")
    return win


def has_target(win):
    print("[DEBUG] Вошли в has_target()")
    if win is None:
        return False

    left = win.left + 780
    top = win.top + 68

    print(f"[DEBUG] Пытаюсь сделать скриншот: left={left}, top={top}")

    try:
        screenshot = pyautogui.screenshot(region=(left, top, 220, 10))
        print("[DEBUG] Скриншот успешно сделан")

        pixels = screenshot.load()
        red_count = 0

        for y in range(screenshot.height):
            for x in range(screenshot.width):
                r, g, b = pixels[x, y]
                if r > 185 and g < 125 and b < 125:
                    red_count += 1

        print(f"[DEBUG] Красных пикселей: {red_count}")
        return red_count >= 25

    except Exception as e:
        print(f"[DEBUG] ОШИБКА: {e}")
        return False


# ====================== Тест ======================

game_window = get_game_window("luk")

if game_window:
    print("\n=== Запуск цикла проверки ===\n")

    try:
        while True:
            result = has_target(game_window)
            status = "ЦЕЛЬ ЕСТЬ" if result else "цели нет"
            print(f"[{time.strftime('%H:%M:%S')}] {status}\n")
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("\nОстановлено.")
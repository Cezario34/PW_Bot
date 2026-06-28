import pyautogui


def has_target(game_window, rel_y=68, check_x_start=780, width=220) -> bool:
    """
    Проверяет наличие цели по красной полоске HP.
    Принимает объект GameWindow.
    """
    if game_window is None or game_window.win is None:
        return False

    left = game_window.left + check_x_start
    top = game_window.top + rel_y

    try:
        screenshot = pyautogui.screenshot(region=(left, top, width, 10))
        pixels = screenshot.load()

        red_count = 0
        for y in range(screenshot.height):
            for x in range(screenshot.width):
                r, g, b = pixels[x, y]
                if r > 185 and g < 125 and b < 125:
                    red_count += 1

        return red_count >= 25

    except:
        return False
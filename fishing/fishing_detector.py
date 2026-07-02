import time
import cv2 as cv
import numpy as np
import mss
import pyautogui
from datetime import datetime
import os
from fish_icon import click_fish_icon
from window.game_window import GameWindow, is_game_active

DEBUG_FOLDER = "debug_fishing"
os.makedirs(DEBUG_FOLDER, exist_ok=True)

# ====================== ГЛОБАЛЬНОЕ СОСТОЯНИЕ ======================
current_success_zone = None
indicator_history = []
MAX_HISTORY = 6


def get_fishing_bar_region(window):
    """Единый источник правды для региона рыболовной полосы"""
    return (
        window.left + 489,
        window.top + 585,
        505,
        18
    )


def analyze_fishing_bar(window):
    if not window or not window.win:
        return False, None

    region = get_fishing_bar_region(window)

    with mss.MSS() as sct:
        screenshot = sct.grab({
            "left": region[0],
            "top": region[1],
            "width": region[2],
            "height": region[3]
        })
        img = np.array(screenshot)
        img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

    # Проверка клёва
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_bite = np.array([0, 45, 50])
    upper_bite = np.array([20, 255, 200])
    mask_bite = cv.inRange(hsv, lower_bite, upper_bite)
    bite_ratio = cv.countNonZero(mask_bite) / (img.shape[0] * img.shape[1])

    has_bite = bite_ratio > 0.35
    print(f"  [DEBUG] bite_ratio = {bite_ratio:.4f} | has_bite = {has_bite}")
    # Поиск индикатора
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(gray)

    print(f"  [DEBUG] max_val = {max_val} | rel_x = {max_loc[0]}")

    indicator_x = None
    if max_val > 225:
        indicator_x = region[0] + max_loc[0]

    return has_bite, indicator_x


def get_success_zone(window):
    if not window or not window.win:
        return None

    region = get_fishing_bar_region(window)
    scan_y = region[1] + 6

    with mss.MSS() as sct:
        screenshot = sct.grab({
            "left": region[0],
            "top": scan_y,
            "width": region[2],
            "height": 3
        })
        img = np.array(screenshot)
        img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

    row = img[1] if img.shape[0] > 1 else img[0]
    mean_color = np.mean(row[:, :3], axis=0)

    success_segments = []
    current_start = None
    current_diff = 0

    for i, pixel in enumerate(row):
        r, g, b = pixel[:3]
        diff = abs(r - mean_color[0]) + abs(g - mean_color[1]) + abs(b - mean_color[2])
        x = region[0] + i

        if diff > 55:
            if current_start is None:
                current_start = x
            current_diff += diff
        else:
            if current_start is not None:
                if current_diff > 0:
                    success_segments.append((current_start, x - 1))
                current_start = None
                current_diff = 0

    if current_start is not None:
        success_segments.append((current_start, region[0] + region[2] - 1))

    if not success_segments:
        return None

    longest = max(success_segments, key=lambda s: s[1] - s[0])
    seg_width = longest[1] - longest[0]

    if seg_width < 20 or seg_width > 220:
        return None

    return longest[0], longest[1]


def save_debug_image(window, indicator_x, success_zone):
    region = get_fishing_bar_region(window)

    with mss.MSS() as sct:
        screenshot = sct.grab({
            "left": region[0],
            "top": region[1],
            "width": region[2],
            "height": region[3]
        })
        img = np.array(screenshot)
        img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

    if success_zone:
        zone_left, zone_right = success_zone
        rel_left = zone_left - region[0]
        rel_right = zone_right - region[0]
        cv.line(img, (rel_left, 2), (rel_right, 2), (0, 255, 0), 2)
        cv.line(img, (rel_left, region[3] - 3), (rel_right, region[3] - 3), (0, 255, 0), 2)

    if indicator_x:
        rel_x = indicator_x - region[0]
        cv.line(img, (rel_x, 0), (rel_x, region[3] - 1), (0, 0, 255), 2)

    timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
    filename = os.path.join(DEBUG_FOLDER, f"bite_{timestamp}.png")
    cv.imwrite(filename, img)
    print(f"  [DEBUG] Сохранена картинка: {filename}")


def predict_and_press(window, indicator_x):
    global current_success_zone

    if indicator_x is None or current_success_zone is None:
        return False

    zone_left, zone_right = current_success_zone
    in_zone = zone_left - 12 <= indicator_x <= zone_right + 10

    print(f"  [DEBUG] in_zone = {in_zone}   (indicator_x = {indicator_x}, зона = {zone_left}-{zone_right})")

    if in_zone:
        print("  [DEBUG] → ЖМЁМ!")

        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        return True

    print("  [DEBUG] → Не жмём: индикатор не в зоне")
    return False


def check_fishing_state(window):
    global current_success_zone, indicator_history

    has_bite, indicator_x = analyze_fishing_bar(window)

    if has_bite:
        if indicator_x:
            print(f"[{time.strftime('%H:%M:%S')}]  КЛЮЁТ!  |  Позиция: {indicator_x}", end="")

            if current_success_zone is None:
                current_success_zone = get_success_zone(window)
                if current_success_zone:
                    save_debug_image(window, indicator_x, current_success_zone)
                    print(f"  [DEBUG] Зона успеха зафиксирована: {current_success_zone}")
                else:
                    print("  [DEBUG] Не удалось захватить зону успеха")

            pressed = predict_and_press(window, indicator_x)
            if not pressed:
                print()
        else:
            print(f"[{time.strftime('%H:%M:%S')}]  КЛЮЁТ!  |  Индикатор не найден")
        return True

    else:
        if current_success_zone is not None:
            print("[DEBUG] Клёв закончился — сбрасываем зону")
            current_success_zone = None
            indicator_history.clear()
        return False


if __name__ == "__main__":

    from window.game_window import GameWindow
    from fish_icon import click_fish_icon, find_fish_icon   # ← добавили find_fish_icon

    game = GameWindow(partial_title="Avelon")
    game.activate()
    time.sleep(1.5)

    print("Бот запущен (логика по иконке). Нажми Ctrl+C для остановки.\n")

    try:
        while True:
            # Проверяем, активно ли окно игры
            if not is_game_active("Avelon"):
                time.sleep(1)
                continue

            game.update_position()

            # === НОВАЯ ЛОГИКА ===
            # Проверяем, есть ли иконка рыбы на экране
            icon_pos = find_fish_icon(game)

            if icon_pos:
                # Иконка есть → значит рыбалка не активна, кликаем
                print("[INFO] Иконка рыбы найдена. Кликаю...")
                pyautogui.rightClick()
                click_fish_icon(game)
                pyautogui.doubleClick()
                time.sleep(1.6)          # даём время на заброс
            else:
                # Иконки нет → значит рыбалка активна, работаем с полосой
                check_fishing_state(game)
                time.sleep(0.03)

    except KeyboardInterrupt:
        print("\nОстановлено.")
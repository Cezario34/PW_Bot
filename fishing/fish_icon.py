import cv2 as cv
import numpy as np
import pyautogui as pg
import mss

def find_fish_icon(window, template_path="image/fish_icon.png"):
    try:
        template = cv.imread(template_path, cv.IMREAD_GRAYSCALE)
        if template is None:
            print(f"[ERROR] Не удалось загрузить шаблон: {template_path}")
            return None

        game_left = window.left
        game_top = window.top
        game_width = window.width
        game_height = window.height

        with mss.MSS() as sct:
            screenshot = sct.grab(
                {
                    "left": game_left,
                    "top": game_top,
                    "width": game_width,
                    "height": game_height
                    }
                )
            img = np.array(screenshot)
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        print(f"[DEBUG] max_val = {max_val:.4f} (чем ближе к 1.0 — тем лучше)")
        confidence = 0.5
        if max_val > confidence:
            h, w = template.shape

            center_x = max_loc[0] + w//2
            center_y = max_loc[1] + h//2
            screen_x = game_left + center_x
            screen_y = game_top + center_y

            return screen_x, screen_y
        else:
            return None
    except Exception as e:
        print(f"[ERROR] Ошибка при поиске иконки: {e}")
        return None

def click_fish_icon(window):
    pos = find_fish_icon(window)
    if pos:
        x, y = pos
        pg.moveTo(x, y, duration=1)
        pg.click()
        print(f"[INFO] Клик по иконке рыбы выполнен ({x}, {y})")
        return True
    else:
        print("[INFO] Иконка рыбы не найдена")
        return False
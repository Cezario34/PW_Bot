import pyautogui
import time

print("Через 3 секунды начнётся захват цвета...")
print("Наведи мышку на СВЕТЯЩУЮСЯ полоску во время клёва\n")
time.sleep(3)

x, y = pyautogui.position()
r, g, b = pyautogui.pixel(x, y)

print(f"Позиция: X={x}, Y={y}")
print(f"Цвет светящейся полоски: RGB=({r}, {g}, {b})")
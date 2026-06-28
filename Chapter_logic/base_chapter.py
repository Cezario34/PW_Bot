import time

import pyautogui as pg

class Chapter:

    def __init__(self, name):
        self.name = name

    def press_button(self, button, duration=0.15):
        pg.keyDown(button)
        time.sleep(duration)
        pg.keyUp(button)

    def step_forward(self, duration=0):
        self.press_button('w', duration)

    def step_back(self, duration=0):
        self.press_button('s', duration)

    def step_left(self, duration=0):
        self.press_button('a', duration)

    def step_right(self, duration=0):
        self.press_button('d', duration)

    def attack(self, duration=0):
        self.press_button('1', duration)

    def press_loot(self, duration=0):
        self.press_button('2', duration)

    def jump(self, duration=0):
        self.press_button('space', duration)

    def find_target(self, duration=0):
        self.press_button('tab', duration)

class WB(Chapter):

    def change_apperance(self):
        self.press_button('5',)

    def agro(self):
        self.press_button('F1')

    def up_shield(self):
        self.press_button('F3')

    def aoe_agro(self):
        self.press_button('F2')

    def debuff_phys(self):
        self.press_button('F4')

    def use_tail(self):
        self.press_button('F5')

    def use_buff(self):
        self.press_button('7')
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from queue import Queue

from Chapter_logic.base_chapter import WB
from window.game_window import GameWindow
from detection.target_detector import has_target

class BotGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot")
        self.root.geometry("720x520")
        self.root.resizable(width=False, height=False)

        self.running = False
        self.bot_thread = None

        self.create_widgets()

    def create_widgets(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=12)

        self.btn_start = tk.Button(
            btn_frame, text="▶ Start", width=14, command=self.start_bot,
            bg="#4CAF50", fg="white", font=("Arial", 11, "bold")
            )
        self.btn_start.pack(side=tk.LEFT, padx=8)

        self.btn_stop = tk.Button(
            btn_frame, text="⏹ Stop", width=14, command=self.stop_bot,
            bg="#f44336", fg="white", font=("Arial", 11, "bold")
            )
        self.btn_stop.pack(side=tk.LEFT, padx=8)
        self.btn_stop.config(state=tk.DISABLED)

        self.btn_exit = tk.Button(
            btn_frame, text="Exit", width=10, command=self.root.quit,
            bg="#555555", fg="white", font=("Arial", 11)
            )
        self.btn_exit.pack(side=tk.LEFT, padx=8)

        tk.Label(self.root, text="Логи:", font=("Arial", 11, "bold")).pack(
            anchor="w", padx=10
            )
        self.log_area = scrolledtext.ScrolledText(
            self.root, width=88, height=24,
            font=("Consolas", 10), state=tk.DISABLED
            )
        self.log_area.pack(padx=10, pady=5)

    def log(self, message: str):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(
            tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n"
            )
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_bot(self):
        if self.running:
            return
        self.running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.log("Бот запускается...")

        self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
        self.bot_thread.start()

    def stop_bot(self):
        self.running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.log("Остановка бота...")

    def bot_loop(self):
        try:
            gw = GameWindow("Avelon Perfect World")
            if not gw.activate():
                self.log("Ошибка: не удалось активировать окно игры")
                self.running = False
                return

            wb = WB("Громобой")
            self.log("Бот успешно запущен")
            count_mobs = 0
            while self.running:
                if not has_target(gw):
                    count_mobs += 1
                    self.log('Ищу таргет')
                    wb.find_target()
                    wb.attack()
                    self.log('Начинаю бить моба')
                    time.sleep(3)
                    self.log("Подобрал лут")
                    self.log(f"бью моба по счету {count_mobs}")


                    if not has_target(gw):
                        wb.press_loot()
                        time.sleep(1)
                        wb.press_loot()
                        self.log("Подобрал лут")
                        self.log(f"Убито мобов {count_mobs}")
                else:
                    wb.press_loot()
                    time.sleep(1)
                    wb.press_loot()
                    self.log('Продолжаю бить моба')

                    wb.attack()
                    time.sleep(3)

                time.sleep(0.3)
                wb.press_loot()
                time.sleep(1)
                wb.press_loot()
        except Exception as e:
            self.log(f"Ошибка: {str(e)}")
        finally:
            self.running = False
            self.root.after(0, lambda: self.btn_start.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_stop.config(state=tk.DISABLED))
            self.log("Бот остановлен.")
from window.game_window import GameWindow
from fishing.fishing_detector import check_fishing_state
import time

game = GameWindow(partial_title="Avelon")
game.activate()

try:
    while True:
        game.update_position()
        check_fishing_state(game)
        # time.sleep(0.6)
except:
    print("\n\nОстановлено.")
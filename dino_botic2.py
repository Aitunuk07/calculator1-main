import pyautogui
import time
import numpy as np
from PIL import ImageGrab

# Настройки
JUMP_KEY = "space"
DUCK_KEY = "down"
GAME_REGION = (300, 400, 1500, 500)  # Область игры (x1, y1, x2, y2)
OBSTACLE_COLOR = (83, 83, 83)       # Цвет препятствий (RGB)
CHECK_DELAY = 0.05                   # Частота проверки (сек)
BIRD_HEIGHT_THRESHOLD = 100          # Высота, ниже которой - птица (пиксели)
OBSTACLE_DETECTION_RANGE = 250       # Насколько далеко смотреть (пиксели)
DUCK_TIME = 0.3                      # Время приседания (сек)

def get_obstacle_info():
    """Определяет тип и расстояние до ближайшего препятствия."""
    screenshot = ImageGrab.grab(bbox=GAME_REGION)
    pixels = np.array(screenshot)
    
    # Ограничиваем область проверки
    obstacle_area = pixels[:, -OBSTACLE_DETECTION_RANGE:]
    obstacle_pixels = np.argwhere(np.all(obstacle_area == OBSTACLE_COLOR, axis=2))
    
    if len(obstacle_pixels) == 0:
        return None, None  # Нет препятствий
    
    min_y = obstacle_pixels[:, 0].min()
    min_x = obstacle_pixels[:, 1].min()
    is_bird = min_y < BIRD_HEIGHT_THRESHOLD
    
    return ("bird" if is_bird else "cactus"), min_x

def press_key(key, hold_time=0.05):
    """Нажимает клавишу и удерживает её нужное время."""
    pyautogui.keyDown(key)
    time.sleep(hold_time)
    pyautogui.keyUp(key)

def main():
    print("🦖 Бот Chrome Dino запущен! (Ctrl+C для остановки)")
    time.sleep(2)
    
    try:
        while True:
            obstacle, distance = get_obstacle_info()
            
            if obstacle and distance:
                if obstacle == "cactus" and distance < 200:
                    press_key(JUMP_KEY)
                    print("🔼 Прыжок через кактус!")
                elif obstacle == "bird" and distance < 220:
                    press_key(DUCK_KEY, DUCK_TIME)
                    print("🔽 Приседание под птицей!")
                    
            time.sleep(CHECK_DELAY)
    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    main()

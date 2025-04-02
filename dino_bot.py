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

def get_obstacle_info():
    """Определяет тип препятствия (кактус или птица) и его положение."""
    screenshot = ImageGrab.grab(bbox=GAME_REGION)
    pixels = np.array(screenshot)
    
    # Ищем пиксели цвета препятствий в правой части экрана
    obstacle_area = pixels[:, -200:]
    obstacle_pixels = np.argwhere(np.all(obstacle_area == OBSTACLE_COLOR, axis=2))
    
    if len(obstacle_pixels) == 0:
        return None  # Нет препятствий
    
    # Определяем минимальную Y-координату препятствия (верхнюю границу)
    min_y = obstacle_pixels[:, 0].min()
    
    # Если верхняя граница выше порога - это птица, иначе - кактус
    is_bird = min_y < BIRD_HEIGHT_THRESHOLD
    return "bird" if is_bird else "cactus"

def press_key(key):
    """Нажимает клавишу."""
    pyautogui.keyDown(key)
    time.sleep(0.05)
    pyautogui.keyUp(key)

def main():
    print("🦖 Умный бот для Chrome Dino запущен! (Ctrl+C для остановки)")
    time.sleep(2)
    
    try:
        while True:
            obstacle = get_obstacle_info()
            
            if obstacle == "cactus":
                press_key(JUMP_KEY)
                print("🔼 Прыжок через кактус!")
            elif obstacle == "bird":
                press_key(DUCK_KEY)
                print("🔽 Приседание под птицей!")
                
            time.sleep(CHECK_DELAY)
    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    main()
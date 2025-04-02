import pyautogui
import time
import numpy as np
from PIL import ImageGrab

# Настройки
JUMP_KEY = "space"
DUCK_KEY = "down"
GAME_REGION = (300, 300, 900, 500)  # Более точная область игры (x1, y1, x2, y2)
OBSTACLE_COLOR = (83, 83, 83)       # Цвет препятствий (RGB)
BACKGROUND_COLOR = (247, 247, 247)   # Цвет фона (RGB)
CHECK_DELAY = 0.05                   # Частота проверки (сек)
BIRD_HEIGHT_THRESHOLD = 100          # Высота, ниже которой - птица (пиксели)
OBSTACLE_WIDTH = 30                  # Ширина области для поиска препятствий

def get_obstacle_info():
    """Определяет тип препятствия (кактус или птица) и его положение."""
    screenshot = ImageGrab.grab(bbox=GAME_REGION)
    pixels = np.array(screenshot)
    
    # Ищем пиксели цвета препятствий в правой части экрана
    obstacle_area = pixels[:, -OBSTACLE_WIDTH:]
    
    # Создаем маску для препятствий (учитываем небольшое отклонение в цвете)
    color_diff = 20
    obstacle_mask = (
        (np.abs(obstacle_area[:, :, 0] - OBSTACLE_COLOR[0]) < color_diff) & \
        (np.abs(obstacle_area[:, :, 1] - OBSTACLE_COLOR[1]) < color_diff) & \
        (np.abs(obstacle_area[:, :, 2] - OBSTACLE_COLOR[2]) < color_diff))
    
    obstacle_pixels = np.argwhere(obstacle_mask)
    
    if len(obstacle_pixels) == 0:
        return None  # Нет препятствий
    
    # Определяем минимальную Y-координату препятствия (верхнюю границу)
    min_y = obstacle_pixels[:, 0].min()
    
    # Если верхняя граница выше порога - это птица, иначе - кактус
    is_bird = min_y < BIRD_HEIGHT_THRESHOLD
    return "bird" if is_bird else "cactus"

def press_key(key, duration=0.05):
    """Нажимает клавишу."""
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def main():
    print("🦖 Умный бот для Chrome Dino запущен! (Ctrl+C для остановки)")
    time.sleep(2)
    last_action = None
    
    try:
        while True:
            obstacle = get_obstacle_info()
            
            if obstacle == "cactus" and last_action != "jump":
                press_key(JUMP_KEY)
                print("🔼 Прыжок через кактус!")
                last_action = "jump"
            elif obstacle == "bird" and last_action != "duck":
                press_key(DUCK_KEY, 0.3)  # Более длительное приседание для птицы
                print("🔽 Приседание под птицей!")
                last_action = "duck"
            else:
                last_action = None
                
            time.sleep(CHECK_DELAY)
    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    main()
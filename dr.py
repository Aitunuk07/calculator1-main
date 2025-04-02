import time
import pyautogui
import mss
import numpy as np

# Координаты области экрана (настрой под себя!)
BBOX = (300, 410, 450, 460)  # x1, y1, x2, y2
JUMP_KEY = "space"
DUCK_KEY = "down"
CHECK_DELAY = 0.1  # Интервал проверки

def get_obstacle_info():
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(BBOX))[:, :, 0]  # Берём только один канал (ч/б)
        
        if np.any(screenshot < 100):  # Есть тёмный объект (кактус или птица)
            obstacle_y = np.where(screenshot < 100)[0]  # Получаем координаты
            if len(obstacle_y) > 0 and np.min(obstacle_y) < 20:  # Если препятствие высоко (птица)
                return "bird"
            return "cactus"
    
    return None

def press_key(key, duration=0.1):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def main():
    print("Бот запущен! Начни игру (нажми пробел) и не трогай клавиатуру.")
    time.sleep(2)  # Ожидание перед стартом

    last_action = None

    try:
        while True:
            obstacle = get_obstacle_info()

            if obstacle == "cactus" and last_action != "jump":
                press_key(JUMP_KEY)
                print("⬆ Прыжок!")
                last_action = "jump"

            elif obstacle == "bird" and last_action != "duck":
                press_key(DUCK_KEY, 0.3)
                print("⬇ Пригибание!")
                last_action = "duck"

            else:
                last_action = None

            time.sleep(CHECK_DELAY)

    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    main()

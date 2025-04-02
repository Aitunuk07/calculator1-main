import time
import pyautogui
import mss
import numpy as np
import cv2

# Координаты области экрана для обнаружения препятствий (нужно настроить)
BBOX = (300, 410, 450, 460)  # x1, y1, x2, y2
JUMP_KEY = "space"
DUCK_KEY = "down"
CHECK_DELAY = 0.05  # Интервал проверки

screenshot = pyautogui.screenshot(region=(300, 410, 150, 50))  # Аналог BBOX
screenshot.save("debug_screenshot.png")
print("Скриншот области сохранён как bbox_screenshot.png")
                                   
def get_obstacle_info():
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(BBOX))[:, :, 0]  # Берем только один канал (черно-белый)
        print(f"Min pixel value: {np.min(screenshot)}")  # Выводит минимальное значение пикселей
        if np.any(screenshot < 100):  # Если есть темный объект (кактус или птица)
            return "obstacle"
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

            if obstacle and last_action != "jump":
                press_key(JUMP_KEY)
                print("⬆ Прыжок!")
                last_action = "jump"
            else:
                last_action = None

            time.sleep(CHECK_DELAY)

    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")

if __name__ == "__main__":
    main()
               
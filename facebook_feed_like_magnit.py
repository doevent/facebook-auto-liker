'''
pip install pyautogui
pip install selenium
pip install pywin32
pip install opencv-python #распознование картинок

'''

import time
import pyautogui #делает скриншот
# import numpy.core.multiarray
# import cv2 # для распознования7
# import random
import datetime
import configparser

# Загрузка настроек из ini файла
try:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    confidence_set = float(config.get("Settings", "confidence")) # Настройки качества картинок
    pause_magnit = int(config.get("Settings", "pause_magnit")) # глобальная пауза в сториес
except Exception as e:
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} >> Ошибка загрузки INI")

# Функция поиска кнопок и цикл лайков
def stories_likes():
        
    #Поиск нопок лайков сториес
    while True:
        try:
            
            x, y = pyautogui.position()
            likeX, likeY = pyautogui.locateCenterOnScreen('img/feed_like.png', grayscale=True)
            
            pyautogui.moveTo(likeX, likeY, 0)
            pyautogui.click(likeX, likeY, duration=0.0) #SUper
            time.sleep(1)
            pyautogui.moveTo(x, y, 0)
            
            time.sleep(pause_magnit)

        except Exception as e:
            time.sleep(1)






if __name__ == "__main__":
    print("Старт программы FACEBOOK - LIKE MAGNIT.")
    stories_likes()
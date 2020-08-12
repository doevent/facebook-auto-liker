# -*- coding: utf8 -*-

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementClickInterceptedException, NoSuchElementException

import time
import random
import datetime
import configparser

import tempfile
import os
import schedule
import time
import telebot
import requests # проверка версии



log_filename = f'fb_log\\facebook_schedule_ru-{datetime.datetime.now().strftime("%d-%m-%Y")}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, filemode='a', format=' %(asctime)s: %(name)s - %(levelname)s - %(message)s')
print(log_filename)
logging.info("==============================================================")
logging.info("Старт программы")



# Загрузка настроек из ini файла
try:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    version = config.get("Settings", "version") # Текущая версия
    chrome_user = config.get("Settings", "chrome_user") # Имя пользователя в браузере Хром
    width_set = int(config.get("Settings", "width")) # Ширина окна браузера
    height_set = int(config.get("Settings", "height")) # Высота окна браузера сториес
    stories_set = int(config.get("Settings", "stories")) # количество циклов сториес
    birthday_set = int(config.get("Settings", "birthday")) # количество циклов поздравления
    feed_set = int(config.get("Settings", "feed")) # количество циклов поздравления
    feed_select = int(config.get("Settings", "feed_select")) # количество циклов поздравления
    API_TOKEN = str(config.get("Settings", "token")) # Токен телеграм бота
    BotID = str(config.get("Settings", "botid")) # ID телеграм бота
    schedule_birthday = str(config.get("Times", "schedule_birthday")) # планировщик поздравлений
    schedule_stories1 = str(config.get("Times", "schedule_stories1")) # планировщик сториес
    schedule_stories2 = str(config.get("Times", "schedule_stories2")) # планировщик сториес
    schedule_stories3 = str(config.get("Times", "schedule_stories3")) # планировщик сториес
    schedule_like_feed1 = str(config.get("Times", "schedule_like_feed1")) # планировщик лайков новостной ленты

    stories_set_end = stories_set - 1 # отнимаем единицу, для условия завешения работы
except Exception as e:
    logging.exception("Ошибка загрузки INI")
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка загрузки INI")

if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
    bot = telebot.TeleBot(API_TOKEN)

# Проверка версии
r_version = 0
upd_version = 0
try:
    r_version = requests.get('https://skobeev.design/fb/version.txt')
    r_version.encoding = 'utf-8' 
    upd_version = r_version.text
    # print(f"Текущая версия: {version}\nПоследняя версия: {r_version.text}")
    logging.info(f"Текущая версия: {version}")
    if upd_version == version:
        print(f"Последняя версия установлена: {version}")
    else:
        print(f"Последняя версия: {upd_version}")
except Exception as e:
    upd_version = "Недоступно"
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка проверки версии.")
    logging.exception('Ошибка проверки версии')


#настройки создания окна хрома
options = webdriver.ChromeOptions() 
options.add_argument("disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f"user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\Google\\Chrome\\User Data\\{chrome_user}")


driver = 0 # селениум
size = 0 # размер окна браузер
position = 0 # позиция окна браузера
print (f"\nРасписание планировщика:\nПоздравления: {schedule_birthday} ч:м\nЛайки сториес: {schedule_stories1} ч:м\nЛайки сториес: {schedule_stories2} ч:м\nЛайки сториес: {schedule_stories3} ч:м\nЛайки ленты: {schedule_like_feed1} ч:м\n\nТекущая версия: {version}\nПоследняя версия: {upd_version}")
print (f"\n{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Режим ожидания...\n")
if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
    bot.send_message(BotID, f"<b>Start FACEBOOK Bot</b>\n\nРасписание планировщика:\nПоздравления: <b>{schedule_birthday}</b> ч:м\nЛайки сториес: <b>{schedule_stories1}</b> ч:м\nЛайки сториес: <b>{schedule_stories2}</b> ч:м\nЛайки сториес: <b>{schedule_stories3}</b> ч:м\nЛайки ленты: {schedule_like_feed1} ч:м\n\nТекущая версия: <b>{version}</b>\nПоследняя версия: <b>{upd_version}</b>\nЛог: {log_filename}\n", parse_mode='Html')


#Функция Создания окна браузера
def start_browser():
    global action
    global driver
    global size
    global position
    try:
        # создаем пустое окно браузера
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Создаем окно браузера...")
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        logging.exception("Ошибка в каталоге TEMP")
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в каталоге TEMP\n{tempfile.gettempdir()}")
        try:
            if os.path.exists(tempfile.gettempdir()) == False:
                logging.warning("Каталог не найден. Создаем новый.\n{tempfile.gettempdir()}")
                os.mkdir(tempfile.gettempdir())
        except Exception as e:
            logging.exception("Ошибка создания каталога в TEMP")
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка создания каталога в TEMP\n{tempfile.gettempdir()}")
    except Exception as e:
        logging.exception('Ошибка создания окна браузера')

        
    # Маскировка браузера от фейсбука
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
        })

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
    # Конец масикровки
    driver.set_window_rect(10,10, width_set, height_set)
    driver.get("chrome://settings/help")
    time.sleep(3)
    
    size = driver.get_window_size()
    position = driver.get_window_position()
    print(f"Window size: width = {size['width']}px, height = {size['height']}px, x = {position['x']}, y = {position['y']}")
    logging.info(f"Window size: width = {size['width']}px, height = {size['height']}px, x = {position['x']}, y = {position['y']}")
    print(driver.capabilities['browserVersion'])
    logging.info(driver.capabilities['browserVersion'])
    ActionChains(driver).send_keys(Keys.ESCAPE).perform() #жмем esc чтобы убрать всплывающие окна
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform() #жмем esc чтобы убрать всплывающие окна
    ActionChains(driver).reset_actions()
    if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
        bot.send_message(BotID, f"<b>Создано новое окно браузера.</b>\n{driver.title}\nВерсия Chrome: {driver.capabilities['browserVersion']}\nWindow size: width = {size['width']}px, height = {size['height']}px,\nx = {position['x']}, y = {position['y']}", parse_mode='Html')
    logging.info("Создано окно браузера.")

#-----------------------------------------------------------
# Старт функции поздравлений
def start_birthday_fb():
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Старт функции поздравлений...")

    start_browser()
    logging.info('Старт сценария поздравлений с днем рождения')
    if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
        bot.send_message(BotID, "<b>Старт</b> сценария поздравлений с днем рождения.", parse_mode='Html')
    

    time.sleep(10)
    driver.get("https://www.facebook.com/")
    driver.implicitly_wait(10) # seconds
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    WebDriverWait(driver, 10)

    ActionChains(driver).send_keys(Keys.ESCAPE).perform() #жмем esc чтобы убрать всплывающие окна
    time.sleep(2)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform() #жмем esc чтобы убрать всплывающие окна
    time.sleep(2)
    ActionChains(driver).send_keys(Keys.HOME).perform() # листаем вверх
    time.sleep(random.randrange(15,20))
    
    try:
        driver.find_element_by_css_selector("[href='/events/birthdays/']").click()
        time.sleep(random.randrange(15,20))
    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Картинка с подарком не найдена.\n{e}")
        logging.warning(f"Картинка с подарком не найдена.\n{e}")
    else:
        try:
            birthday_message() # Если всё ОК, переходим в функцую отправки сообщений
        except Exception as e:
            logging.debug(e)

# Функция отправки поздравлений
def birthday_message():
    driver.implicitly_wait(40) # seconds
    time.sleep(random.randrange(18,27))

    try:
        with open("birthday.txt", "r", encoding="utf-8") as f:
            birthday = f.readlines()
            
            count_post = driver.find_elements_by_css_selector("[method='POST']")
            len_count = len(count_post)
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Найдено полей для поздавлений: {len_count}")
            
            logging.info(f'Найдено полей для поздавлений: {len_count}')
            num_msg = 0 #счетчик отправленных сообщений
            
            for send_msg in range(0, len_count):
                if len_count == 0:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Нет полей поздравлений №: {num_msg}")
                    logging.info(f'Нет полей поздравлений №: {num_msg}')
                    break
                elif send_msg >= birthday_set:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Лимит поздравлений №: {num_msg}")
                    logging.info(f'Лимит поздравлений №: {num_msg}')
                    break

                try:
                    cmess = driver.find_elements_by_css_selector("[method='POST']")
                    cmess[0].location_once_scrolled_into_view
                    txt = str(random.choice(birthday).replace("\n", ""))
                    ActionChains(driver).click(cmess[0]).send_keys_to_element(cmess[0],txt, Keys.ENTER).perform()
                    time.sleep(random.randrange(10,15))
                    # driver.execute_script("window.scrollBy(0,100)")
                    num_msg = num_msg + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Поздравление №: {num_msg}")
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Текст: {txt}")
                    time.sleep(random.randrange(4,7))
                    ActionChains(driver).reset_actions()
                except ElementClickInterceptedException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Не может кликнуть в поле. Поздравление №: {num_msg}.\n{e}")
                    logging.info(e)
                except NoSuchElementException as e:
                    print(e)
                    logging.info(e)
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в цикле отправления поздравлений. Поздравление №: {num_msg}.\n{e}")
                    logging.exception(f"Ошибка в цикле отправления поздравлений. Поздравление №: {send_msg}.\n{e}")
                    break
                    # driver.save_screenshot(f'/screenshots/birthday-{num_msg}.png')
            logging.info(f'Отправлено поздравлений на страницу: {num_msg} из {len_count}')
            print (f"\n\nОправлено сообщений на страницу: {num_msg} из {len_count}\n\nРасписание планировщика:\nПоздравления: {schedule_birthday} ч:м\nЛайки сториес: {schedule_stories1} ч:м\nЛайки сториес: {schedule_stories2} ч:м\nЛайки сториес: {schedule_stories3} ч:м\nЛайки ленты: {schedule_like_feed1} ч:м")
            print (f"\n\n{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Режим ожидания...\n")
            try:
                if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
                    bot.send_message(BotID, f"<b>Конец</b> функции BIRTHDAY.\n\nОправлено на страницу: <b>{num_msg}</b> из <b>{len_count}</b>", parse_mode='Html')
            except Exception as e:
                logging.debug(e)
            f.close()
            try:
                driver.quit()
            except Exception as e:
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка закрытия браузера...")


    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в блоке поздравлений\n{e}\n")
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Прерывание цикла")
        logging.exception("Ошибка в блоке поздравлений.")
        try:
            driver.quit()
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка закрытия браузера...")


#-----------------------------------------------------------
# Начало функций сториес
def start_stories_fb():
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Старт функции STORIES...")
    start_browser() # создаем окно
    logging.info('Старт сценария лайков сториес.')
    
    if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
        bot.send_message(BotID, "Старт сценария лайков сториес.")

    driver.get("https://www.facebook.com/")
    
    driver.implicitly_wait(60) # seconds
    time.sleep(10)
    wait = WebDriverWait(driver, 60)
    
    time.sleep(random.randrange(15,20))
    try:
        driver.find_element_by_css_selector("[aria-label='Все истории']").click()
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка ВСЕ ИСТОРИИ найдена.")
        logging.info("Кнопка ВСЕ ИСТОРИИ НАЙДЕНА.")
        time.sleep(15)

        stories_likes()


    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Не найдена кнопка Все истории \n{e}")
        logging.exception("Не найдена кнопка 'Все истории'.")
        stories_fb_alternative()  # Ищем на странице кнопку, если не найдена, то переходим на альтернатиынй вариант


#альтернативный сценарий входа в сториес
def stories_fb_alternative():
    logging.info("Включение функции альтернативного сценария сториес")
    

    driver.get("https://www.facebook.com/stories")
    driver.implicitly_wait(10) # seconds
    time.sleep(10)
  
    #перемещаемся по ссылкам на сториес человека
    ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB).perform() # нужны три таба, но плюс один когда есть своя сториес.
    time.sleep(random.randrange(5,8))
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    stories_likes() # переходим в функцию поиска кнопок и лайков

# основная функция лайков сториес
def stories_likes():
    #переменные счетчиков
    count_like = 0
    count_super = 0
    count_next = 0
    count_together = 0
    count_skip = 0
    
    next_refrash = 0
    wait = WebDriverWait(driver, 30)
    driver.implicitly_wait(5) # seconds

    #перемещаемся по ссылкам на сториес человека
    ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.RETURN).perform()
    time.sleep(random.randrange(4,8))

    try: # Отключаем звук на компе
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Выключить звук"]'))).click()
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Звук выключен")
    except Exception as e:
        print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка кнопки вкл\выкл звука... \n{e}")
        logging.info("Ошибка кнопки вкл\выкл звука...\n{e}")
        
    try:
        # Цикл лайков
        for stories in range(0, stories_set):
            wait = WebDriverWait(driver, 3)
            rnd_like = random.randrange(1,9)
            # генерация разных сценариев лайков
            if rnd_like == 1:
                # Одинарный лайк
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="1"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка LIKE не найдена.\n{e}")
                    logging.info(f'Like button not \n{e}')
                else:
                    count_like = count_like + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - ЛАЙК...")
                
            elif rnd_like == 2:
                #Одинарный супер
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="2"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка SUPER не найдена.\n{e}")
                    logging.info(f"Блок Сториес. Не найдена кнопка SUPER.\n{e}")
                else:
                    count_super = count_super + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - СУПЕР...")
            
            elif rnd_like == 3:
                # Несколько лайков
                for mkmk in range(0,random.randrange(2,5)):
                    try:
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="1"]'))).click()
                    except Exception as e:
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка LIKE не найдена.\n{e}")
                        logging.info(f'Like button not found\n{e}')
                    else:
                        count_like = count_like + 1
                        time.sleep(random.randrange(0,3))
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - ЛАЙК...")
            
            elif rnd_like == 4:
                # Несколько Супер
                for mkmk in range(0, random.randrange(2,5)):
                    try:
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="2"]'))).click()
                    except Exception as e:
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка SUPER не найдена.\n{e}")
                        logging.info(f"Блок Сториес. Не найдена кнопка SUPER.\n{e}")
                    else:
                        time.sleep(random.randrange(0,3))
                        count_super = count_super + 1
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - СУПЕР...")
            
            elif rnd_like == 5:
                # Лайк + Супер
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="1"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка LIKE не найдена.\n{e}")
                    logging.info(f'Like button not found\n{e}')
                else:
                    count_like = count_like + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - ЛАЙК...")
                    time.sleep(random.randrange(1,4))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="2"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка SUPER не найдена.\n{e}")
                    logging.info(f"Блок Сториес. Не найдена кнопка SUPER.\n{e}")
                else:
                    count_super = count_super + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - СУПЕР...")
            
            elif rnd_like == 6:
                # Супер + Лайк
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="2"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка SUPER не найдена.\n{e}")
                    logging.info(f"Блок Сториес. Не найдена кнопка SUPER.\n{e}")
                else:
                    count_super = count_super + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - СУПЕР...")
                    time.sleep(random.randrange(1,4))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="1"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка LIKE не найдена.\n{e}")
                    logging.info(f'Like button not found\n{e}')
                else:
                    count_like = count_like + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - ЛАЙК...")

            
            elif rnd_like == 7:
                # Лайк, супер, мы вместе
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="1"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка LIKE не найдена.")
                    logging.info(f'Like button not found\n{e}')
                else:
                    count_like = count_like + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - ЛАЙК...")
                    time.sleep(random.randrange(1,4))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="2"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка SUPER не найдена.")
                    logging.info(f"Блок Сториес. Не найдена кнопка SUPER.\n{e}")
                else:
                    count_super = count_super + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - СУПЕР...")
                    time.sleep(random.randrange(0,3))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="16"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка МЫ ВМЕСТЕ не найдена.\n{e}")
                    logging.info(f"Блок Сториес. Не найдена кнопка МЫ ВМЕСТЕ.\n{e}")
                else:
                    count_together = count_together + 1 # счетчик мы вместе
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - МЫ ВМЕСТЕ...")
                    time.sleep(random.randrange(1,4))
                
            elif rnd_like == 8:
                # Мы вместе
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-reaction="16"]'))).click()
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка МЫ ВМЕСТЕ не найдена.\n{e}")
                    logging.info(f"Блок Сториес. Не найдена кнопка МЫ ВМЕСТЕ.\n{e}")
                else:
                    count_together = count_together + 1 # счетчик мы вместе
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - МЫ ВМЕСТЕ..")


            # NEXT
            try:
                wait = WebDriverWait(driver, 3)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '''[aria-label='Кнопка "Следующая подборка"']'''))).click()
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Кнопка: Следующая подборка")
                time.sleep(random.randrange(1,2))
                next_refrash = 0 # clear count error
            except Exception as e:
                try:
                    # print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Не найдена кнопка NEXT. Пробуем второй вариант")
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '''[aria-label='Кнопка "Следующая открытка"']'''))).click()
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Кнопка: Следующая открытка")
                    time.sleep(random.randrange(1,2))
                    next_refrash = 0 # clear count error
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Не найдены обе кнопки NEXT. Обновление...")
                    logging.warning(f"Блок Сториес. Не найдены кнопки NEXT. Останавливаем цикл.\n{e}")
                    
                    next_refrash = next_refrash + 1
                    
                    if next_refrash == 3: # if repeat error no button NEXT - quit browser
                        logging.info("Не найдены кнопки NEXT. Выходим.")
                        driver.quit()
                        break
                    
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Обновление окна.")
                    driver.refresh()
                    time.sleep(random.randrange(10,15))
                    #перемещаемся по ссылкам на сториес человека
                    ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.RETURN).perform()
                    time.sleep(random.randrange(4,8))
                    try: # Отключаем звук на компе
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Выключить звук"]'))).click()
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Звук выключен")
                    except Exception as e:
                        print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка кнопки вкл\выкл звука...\n{e}")
                        logging.info(f"Ошибка кнопки вкл\выкл звука...\n{e}")
                    time.sleep(random.randrange(2,4))
                    logging.info('Refresh browser. No button NEXT')
                    
            
            count_next = count_next + 1
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Листаем...")
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Цикл № {stories} из {stories_set_end} ...")
            time.sleep(random.randrange(2,4))
            
            if stories_set_end == stories: #если цикл закончен, закрываем браузер
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Цикл лайков успешно завершен")
                logging.info(f"Кол-во: {stories} - Цикл лайков успешно завершен.")
                
                driver.quit()
                print (f"\n\nПоставлено лайков: {count_like}\nПоставленно сердечек: {count_super}\nПоставлено Мы вместе: {count_together}\nПролистано: {count_next}\nВсего циклов: {stories + 1}\n\nРасписание планировщика:\nПоздравления: {schedule_birthday} ч:м\nЛайки сториес: {schedule_stories1} ч:м\nЛайки сториес: {schedule_stories2} ч:м\nЛайки сториес: {schedule_stories3} ч:м\nЛайки ленты: {schedule_like_feed1} ч:м\n\n")
                print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Режим ожидания...\n")
                try:
                    if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
                        bot.send_message(BotID, f"Конец функции LIKE STORIES:\n\nПоставлено лайков: {count_like}\nПоставленно сердечек: {count_super}\nПоставлено Мы вместе: {count_together}\nПролистано: {count_next}\nВсего циклов: {stories + 1}")
                except Exception as e:
                    logging.debug(e)
                
    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в блоке цикла генерации вариантов лайков {e}")
        logging.exception("Функция лайков сториес. Ошибка в блоке цикла генерации вариантов лайков")
        driver.quit()


#-----------------------------------------------------------
# Функция начала лайков в ленте
def start_feed_likes():
    logging.info("Старт сценария лайков ленты новостей.")
    if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
        bot.send_message(BotID, "<b>Старт</b> сценария лайков ленты новостей.", parse_mode='Html')

    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Старт функции LIKES FEED...")
    
    start_browser()

    if feed_select == 0:
        driver.get("https://www.facebook.com/")
    else:
        driver.get("https://www.facebook.com/?sk=h_chr")
        
    time.sleep(random.randrange(10,15))
    feed_likes()

# Основная функция лайков
def feed_likes():
    err_like = 0
    #переменные счетчиков
    count_like = 0
    count_super = 0
    count_together = 0
    count_select = 0
    
    # основной цикл
    for x_all in range(0, feed_set):
        time.sleep(random.randrange(1,3))

        ActionChains(driver).send_keys("j").perform()
        time.sleep(random.randrange(6,10))
        ActionChains(driver).send_keys("l").perform()
        ActionChains(driver).reset_actions()
        time.sleep(random.randrange(7,10))

        rnd_like_feed = random.randrange(1,4)
        if rnd_like_feed == 1:
            ActionChains(driver).send_keys(Keys.SPACE).perform() # жмем пробел
            count_like = count_like + 1
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Нравится: {count_like}")

        elif rnd_like_feed == 2:
            ActionChains(driver).send_keys(Keys.TAB).perform() # жмем лево
            time.sleep(random.randrange(2,4))
            ActionChains(driver).send_keys(Keys.SPACE).perform() # жмем пробел
            count_super = count_super + 1
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Супер: {count_super}")

            
        elif rnd_like_feed == 3:
            ActionChains(driver).send_keys(Keys.TAB + Keys.TAB).perform() # жмем лево
            time.sleep(random.randrange(2,4))
            ActionChains(driver).send_keys(Keys.SPACE).perform() # жмем пробел
            count_together = count_together + 1
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Мы вместе: {count_together}")
                    
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Сделано циклов {x_all} из {feed_set - 1}\n")
        ActionChains(driver).reset_actions()
            
        time.sleep(random.randrange(1,5))
        
        
        if x_all == feed_set - 1:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Цикл лайков ленты закончен.")
            print(f"\nНравится: {count_like}\nСупер: {count_super}\nМы вместе: {count_together}\nВсего циклов: {feed_set - 1}\nСделано циклов: {x_all}")
            print (f"\n\nРасписание планировщика:\nПоздравления: {schedule_birthday} ч:м\nЛайки сториес: {schedule_stories1} ч:м\nЛайки сториес: {schedule_stories2} ч:м\nЛайки сториес: {schedule_stories3} ч:м\nЛайки ленты: {schedule_like_feed1} ч:м\n\n")
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Режим ожидания...\n")

            logging.info("Цикл лайков ленты закончен")
            try:
                if API_TOKEN != '0' and BotID != '0' and len(API_TOKEN) > 15 and len(BotID) > 5:
                    bot.send_message(BotID, f"<b>Конец</b> функции <b>ЛАЙКИ ЛЕНТЫ НОВОСТЕЙ</b>:\nНравится: <b>{count_like}</b>\nСупер: <b>{count_super}</b>\nМы вместе: <b>{count_together}</b>\nСделано циклов: <b>{x_all}</b> из <b>{feed_set - 1}</b>", parse_mode='Html')
            except Exception as e:
                logging.debug(e)
            driver.quit()
        
        time.sleep(random.randrange(1,5))


schedule.every().day.at(schedule_birthday).do(start_birthday_fb)
schedule.every().day.at(schedule_stories1).do(start_stories_fb)
schedule.every().day.at(schedule_stories2).do(start_stories_fb)
schedule.every().day.at(schedule_stories3).do(start_stories_fb)
schedule.every().day.at(schedule_like_feed1).do(start_feed_likes)

while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except Exception as e:
        print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в бесконечном цикле... \n{e}\n")
        logging.warning("Ошибка в бесконечном цикле")
        break
        try:
            driver.quit()
        except KeyboardInterrupt:
           print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка, ошибочка.")
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Бесконечный цикл. Браузер не создан:\n driver.quit()")
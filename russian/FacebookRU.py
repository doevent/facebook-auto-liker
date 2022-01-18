# -*- coding: utf8 -*-

# patch chromedriver.exe:  Replacing cdc_ variable ($cdc_asdjflasutopfhvcZLmcfl_)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import Select

import logging
import configparser
import os

import time
import datetime
import random
import requests

import tkinter as tk  # create window
import argparse  # command line


log_filename = f'fb_log\\facebook_select_ru-{datetime.datetime.now().strftime("%d-%m-%Y")}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, filemode='a', format=' %(asctime)s: %(name)s - %(levelname)s - %(message)s')
print(log_filename)
logging.info("==============================================================")
logging.info("Start Script")

# Loading settings from ini file
try:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    chrome_user = config.get("Settings", "chrome_user")  # Username in Chrome browser
    width_set = int(config.get("Settings", "width"))  # Browser window width
    height_set = int(config.get("Settings", "height"))  # Browser window height
    images_set = int(config.get("Settings", "images"))  # turns pictures on and off
    stories_set = int(config.get("Settings", "stories"))  # count of cycle stories
    feed_set = int(config.get("Settings", "feed"))  # count of cycle frends feed
    feed_select = int(config.get("Settings", "feed_select"))  # relevant or new messages in the feed
    API_TOKEN = str(config.get("Settings", "token"))  # Token telegram bot
    BOT_ID = str(config.get("Settings", "botid"))  # Telegram ID of the user to whom to send messages
    DECTECT_POP = bool((config.get("Birthday", "detect_popup")))  # on\off autodetect popup window
    DATE_BIRTHDAY = str(config.get("Birthday", "date"))  # ID last date of congratulation

except Exception as e:
    logging.exception("INI load error")
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> INI load error")


driver = 0
# story counter variables
count_like = 0
count_super = 0
count_together = 0
next_refrash = 0


# The function of sending messages to telegrams
def telegram_sendmsg(bot_message):
    try:
        if API_TOKEN != '0' and BOT_ID != '0' and len(API_TOKEN) > 15 and len(BOT_ID) > 5:
            send_text = 'https://api.telegram.org/bot' + API_TOKEN + '/sendMessage?chat_id=' + BOT_ID + '&parse_mode=Html&text=' + bot_message
            response = requests.get(send_text)
    except Exception as e:
        logging.exception(f"Error send message telegram {e}")


# Browser window creation function
def start_browser():
    global driver

    # chrome window creation settings
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\Google\\Chrome\\User Data\\{chrome_user}")
    if images_set == 0:  # disable pictures
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    try:
        # Create an empty browser window
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Create an empty browser window...")
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        logging.exception("Browser is already running.")
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Browser is already running.")
    except Exception as e:
        logging.exception('Browser is already running.')

    #  Browser Disguise
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
        })

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
    # End of Browser Disguise
    driver.set_window_rect(10, 10, width_set, height_set)
    driver.get("https://facebook.com/")
    time.sleep(3)
    
    size = driver.get_window_size()
    position = driver.get_window_position()
    print(f"Window size: width = {size['width']}px, height = {size['height']}px, x = {position['x']}, y = {position['y']}")
    logging.info(f"Window size: width = {size['width']}px, height = {size['height']}px, x = {position['x']}, y = {position['y']}")
    print(driver.capabilities['browserVersion'])
    logging.info(driver.capabilities['browserVersion'])
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # press esc to remove pop-ups
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # press esc to remove pop-ups
    ActionChains(driver).reset_actions()

    try:
        # Close tabs
        driver.implicitly_wait(7)
        count_close = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Закрыть чат"]')
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Found open tabs: {len(count_close)}")
        for send_close in count_close:
            send_close.click()
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Closed tab")
            time.sleep(5)
            try:
                driver.find_elements(By.CSS_SELECTOR, '[aria-label="ОК"]').click()
                time.sleep(5)
            except Exception as e:
                logging.debug(e)
    except Exception as e:
        logging.debug(e)

    # automatic detect birthdays pop-ups
    if DECTECT_POP is True and DATE_BIRTHDAY != str(datetime.date.today()):
        gift = driver.find_elements(By.CSS_SELECTOR, "[href='/events/birthdays/']")
        if gift:
            start_birthday_fb(auto=True)
            return False
    return True


# -----------------------------------------------------------
# Launch the birthdays function
def start_birthday_fb(auto: bool=False):
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Launch the birthdays function")

    if auto is False:
        start_browser()

    logging.info('Launch the birthdays function')
    telegram_sendmsg("<b>Launch</b> the birthdays function")

    try:
        driver.find_elements(By.CSS_SELECTOR, "[href='/events/birthdays/']")[0].click()
        time.sleep(random.randrange(15, 20))
    except IndexError as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Gift picture not found.")
        logging.debug(f"Gift picture not found.\n{e}")

        driver.implicitly_wait(10)  # seconds
        driver.get("https://www.facebook.com/events/birthdays/")
        time.sleep(random.randrange(40, 50))
        birthday_message(var='alt')
    else:
        birthday_message(var="standard")  # Go to the function of sending messages


# function of sending birthdays
def birthday_message(var: str):
    start_time = time.time()
    driver.implicitly_wait(40)  # seconds
    time.sleep(random.randrange(3, 5))

    with open("birthday.txt", "r", encoding="utf-8") as f:
        birthday = f.readlines()

        count_post = driver.find_elements(By.CSS_SELECTOR, '[method="POST"]')
        len_count = len(count_post)-1
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Найдено полей для поздавлений: {len_count}")

        count_button = len(driver.find_elements(By.CSS_SELECTOR, '[aria-label="Сообщение"]'))
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Найдено кнопок СООБЩЕНИЕ (в личку):  {count_button}")

        logging.info(f'Найдено полей для поздавлений: {len_count}')
        num_msg = 0  # счетчик отправленных хроник
        num_button = 0

    for cv in range(0, 200):  # перебираем элементы и когда элемент окажется тектовым - отправляем поздравление
        ActionChains(driver).send_keys(Keys.TAB).perform()
        element = driver.switch_to.active_element
        # if element.find_elements(By.CSS_SELECTOR, 'span'):
        #     print(element.get_attribute("innerHTML"), "\n")
        driver.implicitly_wait(0)
        if len_count == num_msg or len_count == 0 or num_msg >= 19:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Поздравления в хронике кончились: {num_msg}. Циклов всего: {cv}")
            break
        try:
            if element.find_elements(By.TAG_NAME, 'br')[0].get_attribute('data-text') == 'true':
                try:
                    cmess = driver.find_elements(By.CSS_SELECTOR, '[method="POST"]')
                    txt = str(random.choice(birthday).replace("\n", ""))
                    ActionChains(driver).send_keys_to_element(element, txt, Keys.ENTER).perform()
                    num_msg += 1
                    print(
                        f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Поздравление в хронику №: {num_msg}")
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Текст: {txt}")
                    time.sleep(random.randrange(10, 15))
                    ActionChains(driver).reset_actions()

                except NoSuchElementException as e:
                    print(e)
                    logging.info(e)
                except Exception as e:
                    print(
                        f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в цикле отправления поздравлений. Поздравление №: {num_msg}.\n{e}")
                    logging.exception(f"Ошибка в цикле отправления поздравлений. Поздравление №: {send_msg}.\n{e}")
                    break

        except NoSuchElementException:
            pass
        except Exception as e:
            logging.debug(f"Поздравления в хронику: {e}")

    if var == "standard":  # если запуск не альтернативный, то поздравляем в личку
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Начало поздравлений в личку")
        if count_button != 1 or count_button == 0:  # если 0 и 1 то не перезагружаем страницу
            for t in range(0, 2):
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # жмем esc чтобы убрать всплывающие окна
                time.sleep(2)
            time.sleep(random.randrange(3, 6))

            driver.implicitly_wait(10)
            driver.get("https://www.facebook.com/events/birthdays/")
            time.sleep(random.randrange(15, 30))

        # Поиск кнопки
        try:
            for msgbut in driver.find_elements(By.CSS_SELECTOR,'[aria-label="Сообщение"]'):
                if count_button == num_button or count_button == 0 or num_button >= 15:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Поздравления в личку кончились: {num_button}.")
                    break
                # Клик по кнопке
                try:
                    msgbut.click()
                except Exception as e:
                    break
                    # print(f'Ошибка в клике по кнопке СООБЩЕНИЕ. Пробуем второй способ {e}')
                    # logging.info(f'Ошибка в клике по кнопке СООБЩЕНИЕ. Пробуем второй способ {e}')
                    # ActionChains(driver).move_to_element(msgbut).click().perform()
                time.sleep(random.randrange(30, 40))
                try:
                    element = driver.switch_to.active_element
                    # print(element.get_attribute("outerHTML"), "\n")
                    # print(element.get_attribute("role"))
                    # print(element.parent)
                    if element.get_attribute("role") == "textbox":
                        # print(element.get_attribute("innerHTML"), "\n")
                        txt = str(random.choice(birthday).replace("\n", ""))
                        ActionChains(driver).send_keys(txt, Keys.ENTER).perform()
                        num_button += 1
                        time.sleep(random.randrange(5, 10))
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Поздравление в личку: {num_button}")
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Текст: {txt}")
                        ActionChains(driver).reset_actions()

                        driver.implicitly_wait(20)
                        # закрываем вкладки
                        count_close = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Закрыть чат"]')

                        for send_close in count_close:
                            send_close.click()
                            time.sleep(random.randrange(5, 10))
                            try:
                                driver.find_elements(By.CSS_SELECTOR, '[aria-label="ОК"]')[0].click()
                            except IndexError as e:
                                logging.debug(e)
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Закрыто вкладок: {len(count_close)}")
                        logging.info(f'Закрыто вкладок: {len(count_close)}')
                        time.sleep(random.randrange(15, 20))
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в поле личных сообщений: {e}")
                    logging.exception('Ошибка в поле личных сообщений')
                    break
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в личных сообщениях: {e}")
            logging.warning(f"Ошибка в личных сообщениях: {e}")

    # save date config ini file
    if DECTECT_POP is True and DATE_BIRTHDAY != str(datetime.date.today()):
        config.set("Birthday", "date", str(datetime.date.today()))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
            print(f"DATE: {DATE_BIRTHDAY} vs {datetime.date.today()}")

    logging.info(f'Отправлено поздравлений: {num_msg} из {len_count}')
    print(f"\n\nОправлено поздравлений в хронику: {num_msg} из {len_count}")
    print(f"Оправлено поздравлений в личку: {num_button} из {count_button}")
    print(f'Время выполнения: {round(time.time() - start_time, 1)} секунд')
    print(f"\n\n{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ожидание...\n")

    telegram_sendmsg(f"<b>Конец</b> функции BIRTHDAY.\n\nОправлено в хронику: <b>{num_msg}</b> из <b>{len_count}</b>"
                     f"\nОправлено в личку: <b>{num_button}</b> из <b>{count_button}</b>"
                     f"\nВремя выполнения: <b>{round(time.time() - start_time, 1)}</b> секунд")

    try:
        driver.quit()
    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка закрытия браузера...")


# -----------------------------------------------------------
# Начало функций сториес
def start_stories_fb():
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Старт функции STORIES...")
    brow = start_browser()  # создаем окно
    if brow is False:
        telegram_sendmsg("Skipping the Stories function.")
        driver.quit()
        return None
    logging.info('Старт сценария лайков сториес.')

    telegram_sendmsg("<b>Старт</b> сценария лайков <b>STORIES</b>.")
    
    driver.implicitly_wait(60)  # seconds

    time.sleep(random.randrange(5, 10))
    try:
        hs_button = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Смотреть все истории']")
        if hs_button:
            hs_button[0].click()
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка [Смотреть все истории] найдена.")
            logging.info("Кнопка ВСЕ ИСТОРИИ НАЙДЕНА.")
            time.sleep(20)
            stories_likes()
        else:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Не найдена кнопка '[Смотреть все истории]'. \n{e}")
            logging.exception("Не найдена кнопка '[Смотреть все истории]'.")
            driver.quit()
            return None

    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в кнопке [Смотреть все истории] \n{e}")
        logging.exception("Ошибка в кнопке [Смотреть все истории].")
        stories_fb_alternative()  # Ищем на странице кнопку, если не найдена, то переходим на альтернатиынй вариант


# альтернативный сценарий входа в сториес
def stories_fb_alternative():
    logging.info("Включение функции альтернативного сценария сториес")

    driver.implicitly_wait(15)  # seconds
    driver.get("https://www.facebook.com/stories")
    time.sleep(10)
  
    # перемещаемся по ссылкам на сториес человека
    ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB).perform()  # нужны три таба, но плюс один когда есть своя сториес.
    time.sleep(random.randrange(5, 8))
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    stories_likes()  # переходим в функцию поиска кнопок и лайков


# кнопки лайк, супер и звук и тд...
def stories_button(button, stories=None):
    # переменные счетчиков
    global count_like
    global count_super
    global count_together
    global next_refrash
    
    wait = WebDriverWait(driver, 3)
    driver.implicitly_wait(0)
    
    # Отключаем звук на компе
    if button == 'sound':
        try:
            driver.find_elements(By.CSS_SELECTOR, '[aria-label="Выключить звук"]')[0].click()
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Звук выключен")
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка кнопки вкл\выкл звука...\n{e}")
            logging.info("Ошибка кнопки вкл\выкл звука...\n{e}")
    
    elif button == 'like':
        buttonLIKE = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Нравится"]')
        for btn_like in buttonLIKE:
            try:
                btn_like.click()
                # print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка лайк - найдена...")
                break
            except Exception as e:
                logging.debug('Like button not found')
                # print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка ЛАЙК не найдена. Ищем дальше...")
        count_like = count_like + 1
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - ЛАЙК...")
    elif button == 'love':
        try:
            driver.find_elements(By.CSS_SELECTOR, '[aria-label="Супер"]')[0].click()
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка SUPER не найдена.\n{e}")
            logging.info(f"Блок Сториес. Не найдена кнопка SUPER.\n{e}")
        else:
            count_super += 1
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - СУПЕР...")
    
    elif button == 'cave':
        try:
            driver.find_elements(By.CSS_SELECTOR, '[aria-label="Мы вместе"]')[0].click()
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопка МЫ ВМЕСТЕ не найдена.\n{e}")
            logging.info(f"Блок Сториес. Не найдена кнопка МЫ ВМЕСТЕ.\n{e}")
        else:
            count_together += 1  # счетчик мы вместе
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - МЫ ВМЕСТЕ..")
    elif button == 'next':
        # NEXT
        try:
            wait = WebDriverWait(driver, 1)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '''[aria-label='Кнопка "Следующая подборка"']'''))).click()
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Кнопка: Следующая подборка")
            next_refrash = 0  # clear count error
        except Exception as e:
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '''[aria-label='Кнопка "Следующая открытка"']'''))).click()
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Кнопка: Следующая открытка")
                next_refrash = 0  # clear count error
            except Exception as e:
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Не найдены обе кнопки NEXT. Обновление...")
                logging.debug("Блок Сториес. Не найдены кнопки NEXT. Обновление.")
                
                next_refrash += 1
                
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Обновление окна.")
                logging.info('Refresh browser. No button NEXT')
                driver.get("https://www.facebook.com/stories")
                time.sleep(random.randrange(10, 15))
                # перемещаемся по ссылкам на сториес человека
                try:
                    driver.find_elements(By.LINK_TEXT, 'Воспроизвести все')[0].click()
                except Exception as e:
                    logging.exception("no found text link")
                    driver.quit()

                time.sleep(random.randrange(4, 8))
                try:
                    driver.find_elements(By.CSS_SELECTOR, '[aria-label="Выключить звук"]')[0].click()
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Звук выключен")
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка кнопки вкл\выкл звука...\n{e}")
                    logging.info(f"Ошибка кнопки вкл\выкл звука...\n{e}")


# основная функция лайков сториес
def stories_likes():
    count_next = 0
    count_skip = 0
    global next_refrash
    list_names = []
    start_time = time.time()
    wait = WebDriverWait(driver, 30)
    driver.implicitly_wait(30)  # seconds

    try:
        driver.find_elements(By.LINK_TEXT, 'Воспроизвести все')[0].click()
        print('Кнопка "Воспроизвести все" найдена.')
    except NoSuchElementException:
        print('Кнопка "Воспроизвести все" не найдена.')
        ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB,
                                       Keys.TAB).perform()  # нужны три таба, но плюс один когда есть своя сториес.
        time.sleep(random.randrange(5, 8))
        ActionChains(driver).send_keys(Keys.RETURN).perform()

    driver.implicitly_wait(5)  # seconds
    stories_button('sound')
    try:
        # Главный Цикл лайков
        for stories in range(0, stories_set):
            # wait = WebDriverWait(driver, 4)

            # Находим имя и добавляем в список
            try:
                getms = driver.find_elements(By.CSS_SELECTOR, '[data-pagelet="StoriesContentPane"]')[0].find_elements(By.TAG_NAME, 'img')
                for x in getms:
                    try:
                        if x.get_attribute('height') == "40" and x.get_attribute('width') == "40":
                            # print(x.get_attribute('alt'))
                            getms = x.get_attribute('alt')
                            break
                    except Exception as e:
                        getms = None
                        # list_names = []
                        print(f"Не определилось имя...\n{e}")
                print(getms)
                list_names.append(getms)
                # print(list_names)
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {getms}: {list_names.count(getms)}")
            except Exception as e:
                print("Не найдено")
                print(e)
                # list_names = []
                getms = None

            # Пропускаем длинные сториес
            if list_names.count(getms) >= 4:
                for xm in range(0, 20):

                    try:
                        getms = driver.find_elements(By.CSS_SELECTOR, '[data-pagelet="StoriesContentPane"]')[0].find_elements(By.TAG_NAME, 'img')
                        for x in getms:
                            if x.get_attribute('height') == "40" and x.get_attribute('width') == "40":
                                # print(x.get_attribute('alt'))
                                getms = x.get_attribute('alt')
                                break
                    except Exception as e:
                        print(f"Не определилось имя в пропуске... {e}")
                        list_names = []
                        getms = None

                    if list_names.count(getms) >= 4:
                        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()

                        # NEXT
                        stories_button('next', stories)

                        count_next += 1
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {getms} больше трех раз. Пропускаем.\n")
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Цикл № {stories + 1} из {stories_set} ...")
                    else:
                        break
            else:
                # print(getms.get_attribute("innerHTML"), "\n")

                rnd_like = random.randrange(1, 9)
                # генерация разных сценариев лайков
                if rnd_like == 1:
                    # Одинарный лайк
                    stories_button('like', stories)
                    time.sleep(1)

                elif rnd_like == 2:
                    # Одинарный супер
                    stories_button('love', stories)
                    time.sleep(1)

                elif rnd_like == 3:
                    # Несколько лайков
                    for mkmk in range(0, random.randrange(2, 5)):
                        stories_button('like', stories)
                        time.sleep(1)

                elif rnd_like == 4:
                    # Несколько Супер
                    for mkmk in range(0, random.randrange(2, 5)):
                        stories_button('love', stories)
                        time.sleep(1)

                elif rnd_like == 5:
                    # Лайк + Супер
                    stories_button('like', stories)
                    time.sleep(random.randrange(1, 4))
                    stories_button('love', stories)
                    time.sleep(1)

                elif rnd_like == 6:
                    # Супер + Лайк
                    stories_button('love', stories)
                    time.sleep(random.randrange(1, 4))
                    stories_button('like', stories)
                    time.sleep(1)

                elif rnd_like == 7:
                    # Лайк, супер, мы вместе
                    stories_button('like', stories)
                    time.sleep(random.randrange(1, 4))

                    stories_button('love', stories)
                    time.sleep(random.randrange(2, 4))
                    stories_button('cave', stories)
                    time.sleep(1)

                elif rnd_like == 8:
                    # Мы вместе
                    stories_button('cave', stories)
                    time.sleep(1)

                # driver.get_screenshot_as_file(f"png\\{datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S')}.png")
                # NEXT
                stories_button('next', stories)
                if next_refrash == 3:  # if repeat error no button NEXT - quit browser
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Кнопки не найдены. Закрываем браузер...")
                    logging.warning("Не найдены кнопки NEXT. Закрываем браузер.")
                    driver.quit()
                    break

                count_next += 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Цикл № {stories + 1} из {stories_set} ...")
                time.sleep(random.randrange(2, 4))
            
            if stories_set - 1 == stories:  # если цикл закончен, закрываем браузер
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories + 1} - Цикл лайков успешно завершен")
                logging.info(f"Кол-во: {stories + 1} - Цикл лайков успешно завершен.")
                
                driver.quit()
                print(f"\n\nПоставлено лайков: {count_like}\nПоставленно сердечек: {count_super}\nПоставлено Мы вместе: "
                      f"{count_together}\nПролистано: {count_next}\nВсего циклов: {stories + 1}\nВремя выполнения: "
                      f"{round(time.time() - start_time, 1)} секунд")
                print(f"\n\n{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ожидание...\n")

                telegram_sendmsg(f"<b>Конец</b> функции LIKE STORIES:\n\nПоставлено лайков: <b>{count_like}</b>\nПоставленно сердечек: <b>{count_super}</b>"
                                 f"\nПоставлено Мы вместе: <b>{count_together}</b>\nПролистано: <b>{count_next}</b>"
                                 f"\nВсего циклов: <b>{stories + 1}</b>\nВремя выполнения: <b>{round(time.time() - start_time, 1)}</b> секунд")

                
    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в блоке цикла генерации вариантов лайков {e}")
        logging.exception("Функция лайков сториес. Ошибка в блоке цикла генерации вариантов лайков")
        driver.quit()


# -----------------------------------------------------------
# Функция начала лайков в ленте
def start_feed_likes():
    logging.info("Старт сценария лайков ленты новостей.")

    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Старт функции LIKES FEED...")

    brow = start_browser()  # создаем окно
    if brow is False:
        telegram_sendmsg("Skipping the likes feed function.")
        driver.quit()
        return None
    telegram_sendmsg("<b>Старт</b> сценария лайков ленты новостей.")

    if feed_select != 0:
        driver.get("https://www.facebook.com/?sk=h_chr")

    feed_likes()


# Основная функция лайков ленты друзей
def feed_likes():
    # переменные счетчиков
    count_ad = 0
    count_next = 0
    count_group = 0
    count_like = 0
    count_super = 0
    count_cave = 0
    time.sleep(random.randrange(20, 30))
    start_time = time.time()
    driver.implicitly_wait(0)  # seconds
    # основной цикл
    try:
        for x_all in range(0, feed_set):
            # driver.get_screenshot_as_file(f"png\\{datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S')}.png")
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # жмем esc чтобы убрать всплывающие окна
            time.sleep(random.randrange(1, 3))

            ActionChains(driver).send_keys("j").perform()  # Next Post

            element = driver.switch_to.active_element

            # print(element.get_attribute("innerHTML"), "\n")
            if element.find_elements(By.CSS_SELECTOR, '[dir="ltr"]'):
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Найдено сообщество. Пропускаем...")
                count_group += 1
            elif element.find_elements(By.CSS_SELECTOR, '[aria-label="Реклама"]'):
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Найдена реклама. Пропускаем...")
                count_ad += 1
                time.sleep(random.randrange(3, 6))
            elif element.find_elements(By.CSS_SELECTOR, '[aria-label="Нравится"]'):
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Пост найден. Лайкаем...")

                time.sleep(random.randrange(6, 10))

                ActionChains(driver).send_keys("l").perform()  # Press Like
                ActionChains(driver).reset_actions()
                time.sleep(random.randrange(7, 10))

                rnd_like_feed = random.randrange(1, 4)
                try:
                    if rnd_like_feed == 1:
                        ActionChains(driver).send_keys(Keys.SPACE).perform()  # жмем пробел
                        count_like += 1
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Нравится: {count_like}")

                    elif rnd_like_feed == 2:
                        ActionChains(driver).send_keys(Keys.RIGHT).perform()  # жмем право
                        time.sleep(random.randrange(2, 4))
                        ActionChains(driver).send_keys(Keys.SPACE).perform()  # жмем пробел
                        count_super += 1
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Супер: {count_super}")

                    elif rnd_like_feed == 3:
                        ActionChains(driver).send_keys(Keys.RIGHT, Keys.RIGHT).perform()  # жмем право
                        time.sleep(random.randrange(2, 4))
                        ActionChains(driver).send_keys(Keys.SPACE).perform()  # жмем пробел
                        count_cave += 1
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Мы вместе: {count_cave}")

                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Сделано циклов {x_all + 1} из {feed_set}\n")
                    ActionChains(driver).reset_actions()

                    time.sleep(random.randrange(1, 5))
                except TimeoutException as e:
                    logging.exception(e)
                    break
                except Exception as e:
                    logging.exception(e)
                    break
            else:
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Обнаружен уже поставленный лайк. Пропускаем...")
                count_next += 1

            if x_all == feed_set - 1:
                time.sleep(random.randrange(4, 7))
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Цикл лайков ленты закончен.")
                print(
                    f"\nНравится: {count_like}\nСупер: {count_super}\nМы вместе: {count_cave}"
                    f"\nПропущено рекламы: {count_ad}\nПропущено сообществ: {count_group}\nУже было лайков: {count_next}\nВсего циклов: {feed_set}"
                    f"\nСделано циклов: {x_all + 1}\nВремя выполнения: {round(time.time() - start_time, 1)} секунд")
                print(f"\n\n{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ожидание...\n")
                logging.info("Цикл лайков ленты закончен")

                telegram_sendmsg(f"<b>Конец</b> функции <b>ЛАЙКИ ЛЕНТЫ НОВОСТЕЙ</b>:\nНравится: <b>{count_like}</b>"
                                 f"\nСупер: <b>{count_super}</b>\nМы вместе: <b>{count_cave}</b>\nПропущено рекламы: <b>{count_ad}</b>"
                                 f"\nПропущено сообществ: {count_group}\nУже было лайков: <b>{count_next}</b>\nСделано циклов: <b>{x_all + 1}</b> из <b>{feed_set}</b>"
                                 f"\nВремя выполнения: <b>{round(time.time() - start_time, 1)} секунд</b>")
                driver.quit()

    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Ошибка в блоке лайков ленты друзей {e}")
        logging.exception("Ошибка в блоке лайков ленты друзей")
        driver.quit()


# Отрыть ini файл
def open_file():
    with open('settings.ini', "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Facebook autoclicker")


# Сохранить ini файл
def save_file():
    with open('settings.ini', "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)


window = tk.Tk()
window.title("facebook-auto-liker-bot")
window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED)
btn_open = tk.Button(fr_buttons, text="Открыть", command=open_file)
btn_save = tk.Button(fr_buttons, text="Сохранить", command=save_file)

# Текущая версия: {version}\nПоследняя версия: {upd_version}

button1 = tk.Button(fr_buttons, text="Лайки сториес", bg="blue", fg="yellow", command=start_stories_fb)
button2 = tk.Button(fr_buttons, text="Лайки ленты", bg="orange", fg="blue", command=start_feed_likes)
button3 = tk.Button(fr_buttons, text="Поздравления с ДР", bg="purple", fg="white", command=start_birthday_fb)

label1 = tk.Label(fr_buttons,  text=f"Настройки бота\n")
label2 = tk.Label(fr_buttons,  text=f"\nФункции бота\n")
label4 = tk.Label(fr_buttons,  text=f"\n\nЭта программа написана для тестов\nбраузера на примере facebook."
                                    f"\nИспользуйте на свой страх и риск.\nАвтор не несет ответственности за"
                                    f"\nущерб от данной программы.")

site_link = tk.Entry(fr_buttons)
label1.grid(row=0, column=0)
btn_open.grid(row=1, column=0, sticky="ew")
btn_save.grid(row=2, column=0, sticky="ew")

label2.grid(row=3, column=0)
fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

button1.grid(row=4, column=0)
button2.grid(row=5, column=0)
button3.grid(row=6, column=0)
site_link.grid(row=8, column=0)
site_link.insert(0, 'https://github.com/doevent/facebook-auto-liker')
label4.grid(row=9, column=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?')
    namespace = parser.parse_args()

    # запуск из командной строки
    if namespace.name == 'story':
        start_stories_fb()
    elif namespace.name == 'feed':
        start_feed_likes()
    elif namespace.name == 'birthday':
        start_birthday_fb(auto=False)
    else:
        window.mainloop()

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
import time
import requests # get update version

import tkinter as tk # windows
import argparse # command line


log_filename = f'fb_log\\facebook_select_en-{datetime.datetime.now().strftime("%d-%m-%Y")}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, filemode='a', format=' %(asctime)s: %(name)s - %(levelname)s - %(message)s')
print(log_filename)
logging.info("==============================================================")
logging.info("Start bot")



# get ini
try:
    config = configparser.ConfigParser()
    config.read('settings_en.ini')
    version = config.get("Settings", "version")
    chrome_user = config.get("Settings", "chrome_user")
    width_set = int(config.get("Settings", "width"))
    height_set = int(config.get("Settings", "height"))
    stories_set = int(config.get("Settings", "stories"))
    birthday_set = int(config.get("Settings", "birthday"))
    feed_set = int(config.get("Settings", "feed"))
    feed_select = int(config.get("Settings", "feed_select"))
    schedule_birthday = str(config.get("Times", "schedule_birthday"))
    schedule_stories1 = str(config.get("Times", "schedule_stories1"))
    schedule_stories2 = str(config.get("Times", "schedule_stories2"))
    schedule_stories3 = str(config.get("Times", "schedule_stories3"))
    schedule_like_feed1 = str(config.get("Times", "schedule_like_feed1"))

    
    stories_set_end = stories_set - 1
except Exception as e:
    logging.exception("Error load INI")
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error load INI")

# get new version
r_version = 0
upd_version = 0
try:
    r_version = requests.get('https://skobeev.design/fb/version.txt')
    r_version.encoding = 'utf-8' 
    upd_version = r_version.text
    logging.info(f"Current version: {version}")
    if upd_version == version:
        print(f"Current version: {version}")
    else:
        print(f"Last Version: {upd_version}")
except Exception as e:
    upd_version = "Not available"
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error get version.")
    logging.exception('Error get version')


# Chrome options
options = webdriver.ChromeOptions() 
options.add_argument("disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f"user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\Google\\Chrome\\User Data\\{chrome_user}")


driver = 0
size = 0
position = 0


def start_browser():
    global action
    global driver
    global size
    global position
    try:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Create browser window...")
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        logging.exception("Error TEMP catalog")
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error TEMP catalog\n{tempfile.gettempdir()}")
        try:
            if os.path.exists(tempfile.gettempdir()) == False:
                logging.warning("Directory not found. We create a new.\n{tempfile.gettempdir()}")
                os.mkdir(tempfile.gettempdir())
        except Exception as e:
            logging.exception("Error create TEMP catalog")
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error create TEMP catalog\n{tempfile.gettempdir()}")
    except Exception as e:
        logging.exception('Error Create browser window')

        
    # mask browser
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
        })

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
    
    driver.set_window_rect(10,10, width_set, height_set)
    driver.get("chrome://settings/help")
    time.sleep(3)
    
    size = driver.get_window_size()
    position = driver.get_window_position()
    print(f"Window size: width = {size['width']}px, height = {size['height']}px, x = {position['x']}, y = {position['y']}")
    logging.info(f"Window size: width = {size['width']}px, height = {size['height']}px, x = {position['x']}, y = {position['y']}")
    print(driver.capabilities['browserVersion'])
    logging.info(driver.capabilities['browserVersion'])
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    ActionChains(driver).reset_actions()
    logging.info("Create browser window.")

#-----------------------------------------------------------
def start_birthday_fb():
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Start function of birthday greetings...")

    start_browser()
    logging.info('Start function of birthday greetings')
    
    time.sleep(10)
    driver.get("https://www.facebook.com/")
    driver.implicitly_wait(10) # seconds
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    WebDriverWait(driver, 10)

    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)
    ActionChains(driver).send_keys(Keys.HOME).perform()
    time.sleep(random.randrange(15,20))
    
    try:
        driver.find_element_by_css_selector("[href='/events/birthdays/']").click()
        time.sleep(random.randrange(15,20))
    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Birthday button not found.\n{e}")
        logging.warning(f"Birthday button not found.\n{e}")
    else:
        try:
            birthday_message()
        except Exception as e:
            logging.debug(e)

# function of birthday
def birthday_message():
    driver.implicitly_wait(40) # seconds
    time.sleep(random.randrange(18,27))

    try:
        with open("birthday_en.txt", "r", encoding="utf-8") as f:
            birthday = f.readlines()
            
            count_post = driver.find_elements_by_css_selector("[method='POST']")
            len_count = len(count_post)
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Found fields: {len_count}")
            
            logging.info(f'Found fields: {len_count}')
            num_msg = 0 # counter of sent messages
            
            for send_msg in range(0, len_count):
                if len_count == 0:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> No fields found №: {num_msg}")
                    logging.info(f'No fields found №: {num_msg}')
                    break
                elif send_msg >= birthday_set:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Congratulations limit №: {num_msg}")
                    logging.info(f'Congratulations limit №: {num_msg}')
                    break

                try:
                    cmess = driver.find_elements_by_css_selector("[method='POST']")
                    cmess[0].location_once_scrolled_into_view
                    txt = str(random.choice(birthday).replace("\n", ""))
                    ActionChains(driver).click(cmess[0]).send_keys_to_element(cmess[0],txt, Keys.ENTER).perform()
                    time.sleep(random.randrange(10,15))
                    num_msg = num_msg + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Congratulations №: {num_msg}")
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Text: {txt}")
                    time.sleep(random.randrange(4,7))
                    ActionChains(driver).reset_actions()
                except ElementClickInterceptedException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error click element. Congratulations №: {num_msg}.\n{e}")
                    logging.info(e)
                except NoSuchElementException as e:
                    print(e)
                    logging.info(e)
                except Exception as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error in the congratulations sending cycle. Congratulations №: {num_msg}.\n{e}")
                    logging.exception(f"Error in the congratulations sending cycle. Congratulations №: {send_msg}.\n{e}")
                    break
            logging.info(f'Messages sent: {num_msg} of {len_count}')
            print (f"\n\nMessages sent: {num_msg} of {len_count}")
            print (f"\n\n{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Waiting...\n")
            f.close()
            try:
                driver.quit()
            except Exception as e:
                logging.debug(e)

    except Exception as e:
        logging.exception("Error Messages sent.")
        try:
            driver.quit()
        except Exception as e:
            logging.debug(e)


#-----------------------------------------------------------
def start_stories_fb():
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> START Stories like function...")
    start_browser() # создаем окно
    logging.info('START Stories like function.')
    
    driver.get("https://www.facebook.com/")
    
    driver.implicitly_wait(60) # seconds
    time.sleep(10)
    wait = WebDriverWait(driver, 60)
    
    time.sleep(random.randrange(15,20))
    try:
        driver.find_element_by_css_selector("[aria-label='See all stories']").click()
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Button See all stories FOUND.")
        logging.info("Button See all stories FOUND.")
        time.sleep(15)

        stories_likes()


    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Button See all stories  NOT FOUND.\n{e}")
        logging.exception("Button See all stories  NOT FOUND.")
        driver.quit()

def stories_likes():
 
    count_like = 0
    count_super = 0
    count_next = 0
    count_together = 0
    count_skip = 0
    
    next_refrash = 0
    wait = WebDriverWait(driver, 30)
    driver.implicitly_wait(5) # seconds

    ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.RETURN).perform()
    time.sleep(random.randrange(4,8))

    try: # Sound off
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Mute"]'))).click()
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Mute")
    except TimeoutException as e:
        print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error Mute... \n{e}")
        logging.info("Error Mute...")
        
    try:
        for stories in range(0, stories_set):
            
            rnd_like = random.randrange(1,9)
            if rnd_like == 1:
                # one click like
                buttonLIKE = driver.find_elements_by_css_selector('[aria-label="Like"]')
                for btn_like in buttonLIKE:
                    driver.implicitly_wait(0) # seconds
                    try:
                        btn_like.click()
                        break
                    except Exception as e:
                        logging.debug('Like button not found')
                count_like = count_like + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Like...")
                
            elif rnd_like == 2:
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Love"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Love button not found.")
                    logging.info("Love button not found.")
                count_super = count_super + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Love...")
            
            elif rnd_like == 3:
                for mkmk in range(0,random.randrange(2,5)):
                    buttonLIKE = driver.find_elements_by_css_selector('[aria-label="Like"]')
                    for btn_like in buttonLIKE:
                        driver.implicitly_wait(0) # seconds
                        try:
                            btn_like.click()
                            break
                        except Exception as e:
                            logging.debug('Like button not found')
                    count_like = count_like + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Like...")

            
            elif rnd_like == 4:
                for mkmk in range(0, random.randrange(2,5)):
                    try:
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Love"]'))).click()
                    except TimeoutException as e:
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Love button not found.")
                        logging.info("Love button not found.")
                    time.sleep(random.randrange(0,3))
                    count_super = count_super + 1
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Love...")
            
            elif rnd_like == 5:
                buttonLIKE = driver.find_elements_by_css_selector('[aria-label="Like"]')
                for btn_like in buttonLIKE:
                    driver.implicitly_wait(0) # seconds
                    try:
                        btn_like.click()
                        break
                    except Exception as e:
                        logging.debug('Like button not found')
                count_like = count_like + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Like...")
                time.sleep(random.randrange(1,4))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Love"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Love button not found.")
                    logging.info("Love button not found.")
                count_super = count_super + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Love...")
            
            elif rnd_like == 6:
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Love"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Love button not found.")
                    logging.info("Love button not found.")
                count_super = count_super + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Love...")
                time.sleep(random.randrange(1,4))
                

                buttonLIKE = driver.find_elements_by_css_selector('[aria-label="Like"]')
                for btn_like in buttonLIKE:
                    driver.implicitly_wait(0) # seconds
                    try:
                        btn_like.click()
                        break
                    except Exception as e:
                        logging.debug('Like button not found')
                count_like = count_like + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Like...")

            
            elif rnd_like == 7:
                buttonLIKE = driver.find_elements_by_css_selector('[aria-label="Like"]')
                for btn_like in buttonLIKE:
                    driver.implicitly_wait(0) # seconds
                    try:
                        btn_like.click()
                        break
                    except Exception as e:
                        logging.debug('Like button not found')
                count_like = count_like + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Like...")

                time.sleep(random.randrange(1,4))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Love"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Love button not found.")
                    logging.info("Love button not found.")
                count_super = count_super + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Love...")
                time.sleep(random.randrange(0,3))
                
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Care"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Care button not found.")
                    logging.info("Care button not found.")
                count_together = count_together + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Care...")
                time.sleep(random.randrange(1,4))
                
                
            elif rnd_like == 8:
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Care"]'))).click()
                except TimeoutException as e:
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Care button not found.")
                    logging.info("Care button not found.")
                count_together = count_together + 1
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Care..")
            
            # NEXT
            try:
                wait = WebDriverWait(driver, 3)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Next Bucket Button']"))).click()
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Next Bucket Button")
                time.sleep(random.randrange(1,2))
                next_refrash = 0 # clear count error
            except Exception as e:
                try:
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Next Card Button']"))).click()
                    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Next Card Button")
                    time.sleep(random.randrange(1,2))
                    next_refrash = 0 # clear count error
                except Exception as e:
                    try:
                        wait = WebDriverWait(driver, 3)
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Next bucket Button']"))).click()
                        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Next bucket button")
                        time.sleep(random.randrange(1,2))
                        next_refrash = 0 # clear count error
                    except Exception as e:
                        try:
                            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Next card button']"))).click()
                            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} Next card button")
                            time.sleep(random.randrange(1,2))
                            next_refrash = 0 # clear count error
                        except TimeoutException as e:
                            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Not found NEXT button. Refresh...")
                            logging.warning("Not found NEXT button. Refresh.. ")
                            
                            next_refrash = next_refrash + 1
                            
                            if next_refrash == 3: # if repeat error no button NEXT - quit browser
                                logging.info("Not found NEXT button. Quit.")
                                driver.quit()
                                break
                            
                            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Refresh...")
                            driver.refresh()
                            time.sleep(random.randrange(10,15))
                            ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.RETURN).perform()
                            time.sleep(random.randrange(4,8))
                            try: # Mute
                                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Mute"]'))).click()
                                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Mute")
                            except TimeoutException as e:
                                print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error Mute... \n{e}")
                                logging.info("Error mute...")
                            time.sleep(random.randrange(2,4))
                            logging.info('Refresh browser. No button NEXT')
                    
            
            count_next = count_next + 1
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Next story...")
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> № {stories} of {stories_set_end} ...")
            time.sleep(random.randrange(2,4))
            
            if stories_set_end == stories:
                print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {stories} - Good")
                logging.info(f"Кол-во: {stories} - Good.")
                
                driver.quit()
                print (f"\n\nLikes: {count_like}\nLoves: {count_super}\nCares: {count_together}\nNext: {count_next}\nAll: {stories + 1}")
                print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Waiting...\n")
                
    except Exception as e:
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Error {e}")
        logging.exception("Error likes story")
        driver.quit()


#-----------------------------------------------------------
# Функция начала лайков в ленте
def start_feed_likes():
    logging.info("START news feed like function.")
    print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> START news feed like function...")
    
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
    count_like = 0
    count_super = 0
    count_together = 0
    count_select = 0
    
    for x_all in range(0, feed_set):
        time.sleep(random.randrange(1,3))

        ActionChains(driver).send_keys("j").perform()
        time.sleep(random.randrange(6,10))
        ActionChains(driver).send_keys("l").perform()
        ActionChains(driver).reset_actions()
        time.sleep(random.randrange(7,10))

        rnd_like_feed = random.randrange(1,4)
        if rnd_like_feed == 1:
            ActionChains(driver).send_keys(Keys.SPACE).perform()
            count_like = count_like + 1
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Like: {count_like}")

        elif rnd_like_feed == 2:
            ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(random.randrange(2,4))
            ActionChains(driver).send_keys(Keys.SPACE).perform()
            count_super = count_super + 1
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Love: {count_super}")

            
        elif rnd_like_feed == 3:
            ActionChains(driver).send_keys(Keys.TAB + Keys.TAB).perform()
            time.sleep(random.randrange(2,4))
            ActionChains(driver).send_keys(Keys.SPACE).perform()
            count_together = count_together + 1
            print (f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Care: {count_together}")
                    
        print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> {x_all} of {feed_set - 1}\n")
        ActionChains(driver).reset_actions()
            
        time.sleep(random.randrange(1,5))
        
        
        if x_all == feed_set - 1:
            print(f"{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')} >> Good.")
            print(f"\Likes: {count_like}\Loves: {count_super}\nCares: {count_together}\n{x_all} of {feed_set - 1}")
            logging.info("Good")
            driver.quit()
        
        time.sleep(random.randrange(1,5))

# open ini
def open_file():
    with open('settings_en.ini', "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Facebook autoclicker")

# save ini
def save_file():
    with open('settings_en.ini', "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)


window = tk.Tk()
window.title("facebook-auto-liker-bot")
window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save", command=save_file)

button1 = tk.Button(fr_buttons, text="Like stories", bg="blue", fg="yellow", command=start_stories_fb)
button2 = tk.Button(fr_buttons, text="News feed", bg="orange", fg="blue", command=start_feed_likes)
button3 = tk.Button(fr_buttons, text="Birthday", bg="purple", fg="white", command=start_birthday_fb)

label1 = tk.Label(fr_buttons,  text=f"Settings\n")
label2 = tk.Label(fr_buttons,  text=f"\nFunction\n")
label3 = tk.Label(fr_buttons,  text=f"\n\nCurrent version: {version}\nLast version: {upd_version}")
label4 = tk.Label(fr_buttons,  text=f"\n\nThis program is written for browser tests\non the example of facebook.\nUse at your own risk.\nThe author is not responsible\nfor damage from this program.")

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
label3.grid(row=7, column=0)
site_link.grid(row=8, column=0)
site_link.insert(0,'https://github.com/doevent/facebook-auto-liker')
label4.grid(row=9, column=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
    namespace = parser.parse_args()

    # запуск из командной строки
    if namespace.name == 'story':
        start_stories_fb()
    elif namespace.name == 'feed':
        start_feed_likes()
    elif namespace.name == 'birthday':
        start_birthday_fb()
    else:
        window.mainloop()

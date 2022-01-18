# Facebook Auto Liker (English, Russian)
![alt text](win.jpg)
### version v0.3.1-beta.5
Facebook likes feeds, likes stories, send message birthday.

Автоматический лайкер новостной ленты, историй и отправка поздравлений с днем рождения.

### Functions EN
* Likes friends feed
* Likes stories
* Send Birthday Messages
* Run from the command line

### Функции RU
* Лайки ленты друзей
* Лайки историй
* Поздравления с днем рождения
* Информирование через телеграм бота
* Запуск из командной строки (например для запуска через планировщик)

### Install
 Python: 
```
pip install selenium
```
```
Download Chrome driver https://chromedriver.chromium.org/
```
```
Patch chromedriver.exe:  Replacing cdc_ variable ($cdc_asdjflasutopfhvcZLmcfl_)
```
## Settings

#### Settings
The setting is carried out without a graphical interface in a test format by editing the **setting.ini** file through a text editor or in a built-in text editor.

**chrome_user** - username in the browser (optional). Example:
```
chrome_user = andrey
```
**width** - width of browser window. Example:
```
width = 1024
```
**height** - height of browser window. Example:
```
height = 720
```
**stories** - number of cycles of likes in stories (a large value is not recommended). Example:
```
stories = 150
```
**birthday** - maximum number of congratulations cycles (more than 20 is not recommended). Example:
```
birthday = 19
```
**feed** maximum number of cycles of news feed varnishes (a large value is not recommended). Example:
```
feed = 300
```
**token** - telegram bot token is issued when the bot is created: BotFather (https://t.me/BotFather) Example:
```
token = 1387036342:AAGm4QWD5vUjH7FgQbejmz1jelfvh1WUDQI
```
**botid** - your ID in telegram (not bot). You can find out by sending a message to the bot: getmyid_bot (https://t.me/getmyid_bot). Example:
```
botid = 1251879074
```
#### Setting birthday 
Setting is done by editing the file **birthday.txt**. One congratulations on one line, no hyphenation. Example:
```
Happy Birthday!
Wishing you a Happy Birthday!
Best wishes and a wonderful Birthday!
Happy Birthday! Wishing you all the best on your special day!
Congratulations and best wishes on your Birthday!
I wish you a Happy Birthday and many happy returns of the day!
```
#### Command line
Frends feed likes:
```
python FacebookRU.py feed
FacebookRU.exe feed
```
Likes stories:
```
python FacebookRU.py story
FacebookRU.exe story
```
Birthday:
```
python FacebookRU.py birthday
FacebookRU.exe birthday
```
### Compatibility
* Windows 10, 2019
* Python 3.7+
* Selenium 4.1.0
* Chrome driver current test release version 90.0.4183.87 (for other version: [download driver](https://chromedriver.chromium.org/))
* Chrome current test release 90.0+ (chrome://settings/help)
* Settings Facebook language: Russian, English
* Switch to New Facebook design

## Author
* **Skobeev Maksim** - [DoEvent](https://github.com/doevent/)


## License
This project is licensed under the [MIT](https://en.wikipedia.org/wiki/MIT_License) License

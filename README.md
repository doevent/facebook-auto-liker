# Facebook Auto Liker

### version 0.3.1
Facebook likes feeds, likes stories, send message birthday.

Автоматический лайкер новостной ленты, историй и отправка поздравлений с днем рождения.

### Функции
* Лайки новостной ленты
* Лайки историй
* Поздравления с днем рождения
* Встроенный планировщик
* Информирование через телеграм бота

### Установка
 Python: 
```
pip install selenium
pip install pyTelegramBotAPI
pip install schedule
```
Windows:
```
downloads .exe files
```
## Настройки

#### Настройка параметров
Настройка осуществляется без графического интерфейса в тестовом формате путем редактивания файла **setting.ini** через текстовый редактор или во встроенном текстовым редакторе.

chrome_user - имя пользователя в браузере, если используется. Пример:
```
chrome_user = andrey
```
stories - количество циклов лайков в сториес  (не рекомендуется большое значение). Пример:
```
stories = 150
```
birthday - максимальное количество циклов поздравлений (не рекомендуется большое значение). Пример:
```
birthday = 19
```
feed максимальное количество циклов лаков ленты новостей (не рекомендуется большое значение). Пример:
```
feed = 300
```
токен телеграм бота выдается при созаднии бота: BotFather (https://t.me/BotFather) Пример:
```
token = 1387036342:AAGm4QWD5vUjH7FgQbejmz1jelfvh1WUDQI
```
Ваш ID в телеграме. Можно узнать отправив сообщение боту: getmyid_bot (https://t.me/getmyid_bot). Пример:
```
botid = 1251879074
```
#### Настройка планировщика 
schedule_birthday - время поздравлений в планировщике. Пример:
```
schedule_birthday = 10:00
```
schedule_stories - время лайков в сториес в планировщике. Пример:
```
schedule_stories1 = 10:00
```
schedule_like_feed - время лайков новостной ленты в планировщике. Пример:
```
schedule_like_feed = 15:00
```
#### Настройка поздравлений с днем рождения 
Настройка осуществляется путем редактирования файла **birthday.txt**. Одно поздравление в одну строку, без переносов. Пример:
```
Поздравляю с днем рождения!
Мои поздравления с днем рождения!
Поздравляю с днюшечкой!
Мои поздравления с днюшечкой
Поздравляю с Днем Рождения!
С Днем Рождения тебя!
Прими мои поздравления с днем рождения!
```

### Совместимость
* Python 3.7+
* Selenium 3.4.0+
* Chrome driver current test release 84.0.4147.30 (for other version: [download driver](https://chromedriver.chromium.org/))
* Chrome current test release 84.0+ (chrome://settings/help)
* Option ONLY Russian language facebook interface (Работает только на русскоязычном интерфейсе)
* TODO English version

## Автор
* **Skobeev Maksim** - [DoEvent](https://github.com/doevent/)


## Лицензия
This project is licensed under the [MIT](https://en.wikipedia.org/wiki/MIT_License) License

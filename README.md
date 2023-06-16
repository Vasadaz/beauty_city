# Сайт студии красоты Beauty City
 
Проект `beauty_city` создан для записи в одну из студий красоты Beauty City.
Реализованна онлайн-оплата и сбор заявок для обратного звонка.
О новых заявках сообщает Telegram бот.

[Пример сайта.](https://vasadaz.ru)


## Как установить

1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Vasdaz/beauty_city.git
    ```


2. Установить зависимости:
    ```shell
    pip install -r requirements.txt
    ```

3. [Получить токен Telegram бота.](https://telegram.me/BotFather)


4. [Получить свой Telegram ID.](https://t.me/userinfobot)


5. [Получить токен ЮКасса для тестовых платежей.](https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing)


6. Создать файл `.env` с данными:
    ```dotenv
    ALLOWED_HOSTS=127.0.0.1, localhost # Список разрешённых хостов
    DEBUG=True # Режим отладки Django
    SECRET_KEY=xkiy2...kfr8y
    TELEGRAM_TOKEN=581247650:AAH...H7A # Токен бота Telegram.
    TELEGRAM_CHAT_ID=123456789 # Ваш id Telegram, сюда будут отправлятся отправляться новые заявки.
    YOOMANEY_API_KEY=test_COu...Vko # Токен ЮКасса
    YOOMANEY_SHOP_ID=856541 # ID магазина ЮКасса
    ```


7. Применить миграции:
    ```shell
    python3 manage.py migrate
    ```


8. Создать супер-пользователя для доступа к административной панели Django:
    ```shell
    python3 manage.py createsuperuser
    ```
 

9. Запуск сайта:
    
    ```shell
    python3 manage.py runserver


10. Внесенесите данные через административную панель Django.
     

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
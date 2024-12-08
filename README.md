# Telegram Photo Publisher
Этот скрипт публикует фотографии из заданной директории в Telegram-канал с заданным интервалом. 
Если все изображения будут опубликованы, он перемешает их и начнет публиковать заново.

## Установка
1. Клонируйте репозиторий и перейдите в папку проекта:
```python
git clone https://github.com/ваш-проект.git
cd ваш-проект
```
2. Убедитесь, что у вас установлен Python 3.8 или новее. Установите зависимости:
```python
pip install -r requirements.txt
```
3. Создайте файл `.env` для хранения токена бота и настроек:
```python
NASA_API_KEY=ваш_api_key от NASA
TELEGRAM_BOT_TOKEN=ваш_токен_бота
CHAT_ID=@ваш_канал
PUBLISH_DELAY=14400  # Задержка между публикациями (в секундах), по умолчанию 4 часа
```
* `NASA_API_KEY` — ваш персональный ключ API, который вы можете получить, зарегистрировавшись на сайте NASA API

* `TELEGRAM_BOT_TOKEN` — токен вашего Telegram-бота, полученный от @BotFather.

* `CHAT_ID` — идентификатор вашего канала, например, @YourChannelUsername.

* `PUBLISH_DELAY` — интервал между публикациями в секундах (по умолчанию 4 часа).

4. Убедитесь, что бот добавлен в ваш Telegram-канал с правами администратора.

## Описание скриптов
### 1. Скрипт загрузки изображений SpaceX(`fetch_spacex_images.py`)
Загружает фотографии с последнего или указанного запуска SpaceX.

Пример запуска:
```python
python fetch_spacex_images.py --folder images --launch_id 5eb87d47ffd86e000604b38a
```
* `--folder` — папка для сохранения фотографий (по умолчанию images).
* `--launch_id` — ID запуска SpaceX (опционально).
### 2. Скрипт загрузки изображений APOD (NASA)(`fetch_apod_images.py`)
Загружает изображения APOD из NASA.

Пример запуска:
```python
python fetch_apod_images.py --folder images --count 10
```
* `--folder` — папка для сохранения фотографий (по умолчанию images).
* `--count` — количество изображений для загрузки.

### 3. Скрипт загрузки изображений EPIC (NASA) (`fetch_epic_images.py`)
Загружает изображения EPIC (Earth Polychromatic Imaging Camera) с NASA.

Пример запуска:
```python
python fetch_epic_images.py --folder images --count 5
```
* `--folder` — папка для сохранения фотографий (по умолчанию images).
* `--count` — количество изображений для загрузки.
Этот скрипт обращается к API EPIC, скачивает изображения Земли и сохраняет их в указанной папке.
### 4. Скрипт публикации всех изображений в Telegram(`telegram_bot.py`)
Публикует изображения из заданной директории в Telegram через заданный интервал времени.
Пример запуска:
```python
python publish_images.py --directory images --delay 14400
```
* `--directory` — папка с фотографиями (по умолчанию images).
* `--delay` — задержка между публикациями в секундах (по умолчанию берётся из .env).
Если все фотографии в папке опубликованы, скрипт перемешивает их и публикует заново.

### 5. Вспомогательный скрипт (`utils.py`)

Содержит вспомогательные функции для работы с файлами и загрузкой изображений, которые используются в других скриптах:

`get_file_extension(url)` — извлекает расширение файла из URL.
`downloading_images(url, folder_name, filename)` — загружает изображение из интернета и сохраняет его в указанной папке.
Этот модуль импортируется в другие скрипты и не требует отдельного запуска.


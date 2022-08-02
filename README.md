# Автоматическая публикация фотографий SpaceX и NASA в Telegram-канале

## Установка

- Скачайте код.
- Установите актуальную версию poetry в `UNIX`-подобных дистрибутивах с помощью команды:
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```
или в `Windows Powershell`:
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
- Добавьте к переменной окружения `$PATH` команду poetry:
```
source $HOME/.poetry/bin
```
- Установите виртуальное окружение в директории с проектом командой:
```
poetry config virtualenvs.in-project true
```
- Установите все зависимости (для установки без dev зависимостей можно добавить аргумент `--no-dev`):
```
poetry install
```
- Активируйте виртуальное окружение командой: 
```
source .venv/bin/activate
```

## Настройка переменных окружения

- Cоздайте файл `.env` в директории проекта, на основе файла `.env.example` командой 
(при необходимости скорректируйте значения переменных окружения):
```
cp .env.example .env
```
<details>
  <summary>Переменные окружения</summary>
  <pre>
    IMG_PATH=images
    SPACE_X_URL=https://api.spacexdata.com
    SPACE_X_URI_LATEST=/v5/launches/latest
    SPACE_X_URI_LAUNCH_ID=/v5/launches/
    NASA_API_KEY=bDx2bd83nHdbZdodmq7jdodmpxZwebexheEwbexw
    NASA_URL=https://api.nasa.gov
    NASA_URI_APOD=/planetary/apod
    NASA_URI_EPIC=/EPIC/api/natural/images
    NASA_URI_EPIC_ARCHIVE=/EPIC/archive/natural
    TIMEOUT=10
    RETRY_COUNT=5
    STATUS_FORCE_LIST=429,500,502,503,504
    ALLOWED_METHODS=HEAD,GET,OPTIONS
  </pre>
</details>

***Значение переменной окружения `NASA_API_KEY` здесь указано для примера, с данным значением скрипт работать не будет***

- Нужно получить активный `NASA_API_KEY` на официальном сайте [Nasa](https://api.nasa.gov/). Нужно перейти в меню Generate API Key и заполнить небольшую форму.

## Запуск линтеров

```
flake8 . && mypy . && isort .
```

## Запуск скрипта по скачиванию фотографий при помощи SpaceX API

- Для запуска скрипта по скачиванию фотографий при помощи SpaceX API вводим команду:
```
python3 fetch_spacex_images.py
```
- Есть возможность указать значение уникального идентификатора запуска:

- `-i` или `--launch-id` c указанием уникального идентификатора запуска. По умолчанию значение равно "latest". В этом случае будут выбраны фото с последнего запуска. 
```
python3 fetch_spacex_images.py -i 5eb87d42ffd86e000604b384
```

## Запуск скрипта по скачиванию фотографий при помощи NASA APOD API

- Для запуска скрипта по скачиванию фотографий при помощи NASA APOD API вводим команду:
```
python3 fetch_nasa_apod_images.py
```
- Есть возможность указать значение кол-ва фото для скачивания:

- `-с` или `--images-count` c указанием кол-ва фото. По умолчанию значение равно 30. 
```
python3 fetch_nasa_apod_images.py -c 50
```

## Запуск скрипта по скачиванию фотографий при помощи NASA EPIC API

- Для запуска скрипта по скачиванию фотографий при помощи NASA EPIC API вводим команду:
```
python3 fetch_nasa_epic_images.py
```

## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).

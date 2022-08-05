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
    NASA_API_KEY=
    NASA_URL=https://api.nasa.gov
    NASA_URI_APOD=/planetary/apod
    NASA_URI_EPIC=/EPIC/api/natural/images
    NASA_URI_EPIC_ARCHIVE=/EPIC/archive/natural
    NASA_APOD_IMAGES_COUNT=30
    TIMEOUT=10
    RETRY_COUNT=5
    STATUS_FORCE_LIST=429,500,502,503,504
    ALLOWED_METHODS=HEAD,GET,OPTIONS
    TG_BOT_TOKEN=
    TG_CHAT_ID=
    TG_MAX_LIMIT_UPLOAD_FILE=10000000
    PUBLISH_IMAGE_TIMEOUT=4
  </pre>
</details>

*** Для работы скриптов `fetch_nasa_apod_images.py`, `fetch_nasa_epic_images.py` необходимо заполнить переменную окружения `NASA_API_KEY` активным api ключом. Подробности на официальном сайте [Nasa](https://api.nasa.gov/). Нужно перейти в меню Generate API Key и заполнить небольшую форму.***

*** Для работы скриптов `auto_publish_images.py`, `publish_images.py` необходимо заполнить переменные окружения `TG_BOT_TOKEN`, `TG_CHAT_ID`. Необходимо также создать бота, канал и дать права администратора боту для постинга в канал Telegram. ***

## Запуск линтеров

```
isort . && flake8 . && mypy .
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

## Запуск скрипта публикации фотографии в Telegram канале

- Для запуска скрипта публикации фотографии в Telegram канале вводим команду:
```
python3 publish_images.py
```
В данном случае будет опубликовано случайное фото из директории, которая указана в переменной окружения `IMG_PATH`. В случае, если такой директории нет или она пуста, то ничего не опубликуется в канал Telegram.
В случае, если размер скачанного фото более, чем значение в переменной окружения `TG_MAX_LIMIT_UPLOAD_FILE` (по умолчанию оно равно 10 Мб), то размер фото будет уменьшено до необходимого размера.
- Есть возможность указать имя файла с фото для публикации в канале Telegram:

- `-f` или `--image-filename` c указанием имени файла с фотографией. По умолчанию будет опубликована случайная фотография из директории, которая указана в переменной окружения `IMG_PATH`.

```
python3 publish_images.py -f nasa_apod_1.jpg
```

## Запуск скрипта автопубликации фотографий в Telegram канале

- Для запуска скрипта автопубликации фотографий в Telegram канале вводим команду:
```
python3 auto_publish_images.py
```
В данном случае будет опубликованы все фотографии из директории, которая указана в переменной окружения `IMG_PATH`. В случае, если такой директории нет или она пуста, то ничего не опубликуется в канал Telegram и скрипт закончит свою работу.
В противном случае будут опубликованы фотографии из той же директории, с тайм-аутом, который по умолчанию равен 4 часам. При желании это значение можно скорректировать через переменную окружения `PUBLISH_IMAGE_TIMEOUT`.
В случае, если размер скачанного фото более, чем значение в переменной окружения `TG_MAX_LIMIT_UPLOAD_FILE` (по умолчанию оно равно 10 Мб), то размер фото будет уменьшено до необходимого размера.
- Есть возможность указать значение тайм-аута для следующей публикации фото в канал Telegram:

- `-t` или `--publish-timeout` c указанием значения тайм-аута в часах для следующей публикации фото в канале. По умолчанию это значение составляет 4 часа.

```
python3 auto_publish_images.py -t 2
```

## Пример использования данного набора скриптов

Рекомендуемый порядок запуска скриптов следующий:
```
python3 fetch_spacex_images.py
```
```
python3 fetch_nasa_epic_images.py
```
```
python3 fetch_nasa_apod_images.py
```
```
python3 publish_images.py 
```
```
python3 auto_publish_images.py 
```
Также использовать передачу аргументов, исходя из необходимости.

## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).

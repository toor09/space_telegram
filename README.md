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
    HUBBLE_PHOTO_URL=https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg
    HUBBLE_PHOTO_FILE_NAME=hubble.jpeg
    SPACE_X_URL=https://api.spacexdata.com
    SPACE_X_URI_LATEST=/v5/launches/latest
    NASA_API_KEY=bDx2bd83nHdbZdodmq7jdodmpxZwebexheEwbexw
    NASA_URL=https://api.nasa.gov
    NASA_URI_APOD=/planetary/apod
    NASA_URI_EPIC=/EPIC/api/natural/images
    NASA_URI_EPIC_ARCHIVE=/EPIC/archive/natural
    NASA_APOD_IMAGES_COUNT=30
  </pre>
</details>

## Запуск линтеров

```
flake8 . && mypy . && isort .
```

## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).

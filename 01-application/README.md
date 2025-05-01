# Echo-server на FastAPI

## Описание

Простое веб-приложение на FastAPI, которое предоставляет три эндпоинта:
- `/host` — возвращает имя хоста
- `/ip` — возвращает IP-адрес хоста
- `/author` — возвращает имя автора из переменной окружения `AUTHOR`

## Переменные окружения

- `AUTHOR` — имя автора (обязательно для корректного ответа на `/author`)

## Локальный запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export AUTHOR="Ваше Имя"
python main.py
```

Приложение будет доступно на http://localhost:8000

## Сборка Docker-образа

```bash
docker build -t <dockerhub-username>/echo-server:latest .
```

## Запуск контейнера

```bash
docker run -d -p 8000:8000 --env AUTHOR="Ваше Имя" <dockerhub-username>/echo-server:latest
```

## Публикация образа в Docker Hub

```bash
docker login
docker tag <local-image-id> <dockerhub-username>/echo-server:latest
docker push <dockerhub-username>/echo-server:latest
```

## Пример запросов

```bash
curl http://localhost:8000/host
curl http://localhost:8000/ip
curl http://localhost:8000/author
```

### Примеры ответов

- **GET /host**
    ```json
    {"host": "my-hostname"}
    ```

- **GET /ip**
    ```json
    {"ip": "192.168.1.10"}
    ```

- **GET /author**
    ```json
    {"author": "Ваше Имя"}
    ```

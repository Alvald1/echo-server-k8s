"""
FastAPI приложение для получения информации о хосте, IP-адресе и авторе.

Эндпоинты:
- GET /host   : возвращает имя хоста.
- GET /ip     : возвращает IP-адрес хоста.
- GET /author : возвращает имя автора из переменной окружения AUTHOR (или 'unknown').
"""

from fastapi import FastAPI
import socket
import os


app = FastAPI()


@app.get("/host")
async def get_host():
    """Возвращает имя хоста."""
    return {"host": socket.gethostname()}


@app.get("/ip")
async def get_ip():
    """Возвращает IP-адрес хоста."""
    ip = socket.gethostbyname(socket.gethostname())
    return {"ip": ip}


@app.get("/author")
async def get_author():
    """Возвращает имя автора из переменной окружения AUTHOR (или 'unknown')."""
    author = os.environ.get("AUTHOR")
    if not author:
        author = "unknown"
    return {"author": author}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

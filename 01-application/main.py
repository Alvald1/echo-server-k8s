"""
FastAPI приложение для получения информации о хосте, IP-адресе и авторе.

Эндпоинты:
- GET /host   : возвращает имя хоста.
- GET /ip     : возвращает IP-адрес хоста.
- GET /author : возвращает имя автора из переменной окружения AUTHOR (или 'unknown').
"""

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
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
    return {"author": author}


@app.get("/health/ready")
async def readiness_probe():
    """Readiness probe endpoint."""
    author = os.environ.get("AUTHOR")
    if not author:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not ready"})
    return {"status": "ready"}


@app.get("/health/live")
async def liveness_probe():
    """Liveness probe endpoint."""
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "not alive"})
    return {"status": "alive"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

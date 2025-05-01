from fastapi import FastAPI
import socket

app = FastAPI()


@app.get("/host")
async def get_host():
    return {"host": socket.gethostname()}


@app.get("/ip")
async def get_ip():
    # ...реализация будет добавлена позже...
    pass


@app.get("/author")
async def get_author():
    # ...реализация будет добавлена позже...
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

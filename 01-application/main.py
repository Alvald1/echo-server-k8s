from fastapi import FastAPI
import socket
import os
from dotenv import load_dotenv


app = FastAPI()


@app.get("/host")
async def get_host():
    return {"host": socket.gethostname()}


@app.get("/ip")
async def get_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return {"ip": ip}


@app.get("/author")
async def get_author():
    load_dotenv(override=True)
    author = os.environ.get("AUTHOR")
    if not author:
        author = "unknown"
    return {"author": author}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

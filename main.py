import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

def reply(user_text: str) -> str:
    t = (user_text or "").lower()
    if "привет" in t or "здравствуй" in t:
        return "Привет! Как твои дела?"
    elif "погода" in t:
        return "К сожалению, я не могу проверить погоду. Я всего лишь учебный бот!"
    elif "имя" in t:
        return "Меня зовут Ботти, приятно познакомиться!"
    elif "пока" in t or "до свидания" in t:
        return "До встречи! Хорошего дня!"
    return "Извините, я не совсем понимаю. Можете переформулировать вопрос?"


async def process_and_reply(ws: WebSocket, text: str):
    await asyncio.sleep(3)
    await ws.send_text(reply(text))

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            text = await ws.receive_text()
            asyncio.create_task(process_and_reply(ws, text))
    except WebSocketDisconnect:
        pass

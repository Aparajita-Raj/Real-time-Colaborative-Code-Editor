from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
app = FastAPI(title="PairCode")
rooms = {}
@app.get("/")
def home():
    return HTMLResponse((Path("app/static/index.html")).read_text())
@app.websocket("/ws/{room}")
async def socket(ws: WebSocket, room: str):
    await ws.accept()
    state = rooms.setdefault(room, {"clients": set(), "code": ""})
    state["clients"].add(ws)
    async def send(payload, exclude=None):
        dead=[]
        for client in list(state["clients"]):
            if client is exclude: continue
            try: await client.send_text(json.dumps(payload))
            except Exception: dead.append(client)
        for client in dead: state["clients"].discard(client)
    await ws.send_text(json.dumps({"type":"init","code":state["code"],"users":len(state["clients"])}))
    await send({"type":"presence","users":len(state["clients"])}, ws)
    try:
        while True:
            msg=json.loads(await ws.receive_text())
            if msg.get("type")=="code":
                state["code"]=str(msg.get("code",""))[:100000]
                await send({"type":"code","code":state["code"]}, ws)
    except WebSocketDisconnect:
        state["clients"].discard(ws)
        await send({"type":"presence","users":len(state["clients"])})
        if not state["clients"]: rooms.pop(room,None)

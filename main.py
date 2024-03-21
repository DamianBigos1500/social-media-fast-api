from typing import List
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from api.routes import router as api_router
from core.database import Base, engine


app = FastAPI()


def init_app():
    app = FastAPI(
        title="Social media",
        description="social media fastapi angular app",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        Base.metadata.create_all(bind=engine)

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await db.close()

    return app


app = init_app()

origins = [
    "http://localhost:4200",
    "http://localhost:4000",
    "https://localhost.4200",
    "http://localhost",
    "http://localhost",
    "http://localhost:8080",
    "http://daravix.smarthost.pl/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)


# @app.get("/")
# def health_check():
#     return JSONResponse(content={"status": "Running!"})


class ConnectionManager:
    def __init__(self):
        self.activate_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activate_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.activate_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.activate_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_end(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message {client_id} says {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left chat")


templates = Jinja2Templates(directory="templates")


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def read_item(request: Request, full_path: str):
    return templates.TemplateResponse(request=request, name="index.html")

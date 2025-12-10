from typing import Dict, Set
from fastapi import WebSocket

class WebSocketManager:
    
    def __init__(self):
        self.connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault(run_id, set()).add(websocket)

    def disconnect(self, run_id: str, websocket: WebSocket):
        if run_id in self.connections:
            self.connections[run_id].discard(websocket)
            if not self.connections[run_id]:
                del self.connections[run_id]

    async def send(self, run_id: str, message: dict):
        if run_id not in self.connections:
            return

        dead_sockets = []

        for websocket in self.connections[run_id]:
            try:
                await websocket.send_json(message)
            except Exception:
                dead_sockets.append(websocket)

        for ws in dead_sockets:
            self.disconnect(run_id, ws)


ws_manager = WebSocketManager()

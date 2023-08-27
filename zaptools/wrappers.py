import json
from typing import Any
from fastapi import WebSocket
from .models import Event, EventFactory
from .protocols import ZapClient

class FastApiWSWrapper(ZapClient):
    id:str
    def __init__(self, ws: WebSocket, id:str) -> None:
        self.wsc = ws
        self.id = id
    
    async def send_event(self, event_name:str, payload: Any):
        new_event = Event(event_name, payload)
        event_dict = EventFactory.event_to_dict(new_event)
        data = json.dumps(event_dict, indent=4)
        await self.wsc.send_json(data, mode="binary")

    async def close_conection(self):
        await self.wsc.close()

class AnyClient(ZapClient):
    ...
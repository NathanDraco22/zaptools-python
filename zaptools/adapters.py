from typing import Any
import json

EVENT_KEY= "eventName"
PAYLOAD_KEY = "payload"

class FastApiAdapter:

    websocket:Any

    def __init__(self, websocket) -> None:
        self.websocket = websocket

    async def start_connection(self):
        await self.websocket.accept()

    async def recv_json(self) -> dict[str, Any]:
        return await self.websocket.receive_json()

    async def send_event(self, event_name:str, payload:Any):
        json_dict = {
            EVENT_KEY : event_name,
            PAYLOAD_KEY : payload
        }
        await self.websocket.send_json(json_dict)
    
    async def close(self):
        await self.websocket.close()

class SanicAdapter:

    websocket:Any

    def __init__(self, websocket) -> None:
        self.websocket = websocket

    async def start_connection(self):
        ...

    async def recv_json(self) -> dict[str, Any]:
        data = await self.websocket.recv()
        json_data = json.loads(data)
        return json_data
    
    async def send_event(self, event_name:str, payload:Any):
        json_dict = {
            EVENT_KEY : event_name,
            PAYLOAD_KEY : payload
        }
        json_str = json.dumps(json_dict)
        await self.websocket.send(json_str)
    
    async def close(self):
        await self.websocket.close()
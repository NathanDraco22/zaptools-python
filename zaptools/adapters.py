import asyncio
from typing import Any, AsyncIterator
import json

EVENT_KEY= "eventName"
PAYLOAD_KEY = "payload"
HEADERS_KEY = "headers"

class FastApiAdapter:

    websocket:Any

    def __init__(self, websocket) -> None:
        self.websocket = websocket

    async def start_connection(self):
        await self.websocket.accept()

    async def recv_json(self) -> dict[str, Any]:
        return await self.websocket.receive_json()

    def send_event(self, event_name:str, payload:Any, headers: dict[str, Any]):
        json_dict = {
            EVENT_KEY : event_name,
            PAYLOAD_KEY : payload,
            HEADERS_KEY : headers
        }
        asyncio.create_task(self.websocket.send_json(json_dict))
    
    async def json_event_stream(self) -> AsyncIterator[Any]:
        async for data in self.websocket.iter_json():
            yield data
    
    def close(self):
        asyncio.create_task(self.websocket.close())

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
    
    def send_event(self, event_name:str, payload:Any):
        json_dict = {
            EVENT_KEY : event_name,
            PAYLOAD_KEY : payload
        }
        json_str = json.dumps(json_dict)
        asyncio.create_task(self.websocket.send(json_str))
    
    def close(self):
        asyncio.create_task(self.websocket.close())
    
    async def json_event_stream(self) -> AsyncIterator:
        async for data in self.websocket:
            json_data = json.loads(data)
            yield json_data
    
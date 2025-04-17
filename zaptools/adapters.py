from typing import Any, AsyncIterator
import json

from .protocols import ConnectionAdapter

EVENT_KEY = "eventName"
PAYLOAD_KEY = "payload"
HEADERS_KEY = "headers"


class FastApiAdapter(ConnectionAdapter):

    websocket: Any

    def __init__(self, websocket: Any) -> None:
        self.websocket = websocket

    async def start_connection(self):
        await self.websocket.accept()

    async def recv_json(self) -> dict[str, Any]:
        return await self.websocket.receive_json()

    async def send_event(
        self,
        event_name: str,
        payload: Any,
        headers: dict[str, Any] | None = None,
    ):
        json_dict: dict[str, Any] = {
            EVENT_KEY: event_name,
            PAYLOAD_KEY: payload,
        }

        if headers:
            json_dict[HEADERS_KEY] = headers

        await self.websocket.send_json(json_dict)

    async def json_event_stream(self) -> AsyncIterator[Any]:
        async for data in self.websocket.iter_json():
            yield data

    async def close(self):
        await self.websocket.close()


class SanicAdapter(ConnectionAdapter):

    websocket: Any

    def __init__(self, websocket: Any) -> None:
        self.websocket = websocket

    async def start_connection(self): ...

    async def recv_json(self) -> dict[str, Any]:
        data = await self.websocket.recv()
        json_data = json.loads(data)
        return json_data

    async def send_event(
        self,
        event_name: str,
        payload: Any,
        headers: dict[str, Any] | None = None,
    ):
        json_dict: dict[str, Any] = {
            EVENT_KEY: event_name,
            PAYLOAD_KEY: payload,
        }

        if headers:
            json_dict[HEADERS_KEY] = headers

        json_str = json.dumps(json_dict)
        await self.websocket.send(json_str)

    async def close(self):
        await self.websocket.close()

    async def json_event_stream(self) -> AsyncIterator[Any]:
        async for data in self.websocket:
            json_data = json.loads(data)
            yield json_data

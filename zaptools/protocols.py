from typing import Protocol, Coroutine, runtime_checkable

@runtime_checkable
class WebSocketClient(Protocol):
    async def send_event(self, event_name:str, payload: dict) -> Coroutine:
        ...
    async def close_conection(self) -> Coroutine:
        ...

@runtime_checkable
class WebSocketEvent(Protocol):
    name:str
    payload:str
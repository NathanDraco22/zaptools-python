from typing import Protocol, Coroutine, Any, runtime_checkable

@runtime_checkable
class ZapClient(Protocol):
    id:str
    async def send_event(self, event_name:str, payload: Any) -> Coroutine:
        ...
    async def close_conection(self) -> Coroutine:
        ...

@runtime_checkable
class ZapEvent(Protocol):
    name:str
    payload:str
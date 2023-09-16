from typing import Protocol, Any, Callable, AsyncIterator

class ConnectionAdapter(Protocol):

    websocket:Any

    def __init__(self, websocket) -> None:
        self.websocket = websocket

    async def start_connection(self):
        ...

    async def recv_json(self) -> dict[str, Any]:
        ...
    
    async def json_event_stream(self) -> AsyncIterator:
        ...
    
    async def send_event(self, event_name:str, payload:Any, headers: dict[str, Any]):
        ...
    
    async def close(self):
        ...

class Event(Protocol):
    name: str
    callback: Callable

class EventBook(Protocol):
    event_records: dict[str, Event]

    def save_event(self, event: Event):
        ...

    def get_event(self, name:str) -> Event|None:
        ...

class IDController(Protocol):
    _ID_HEADING = "zpt"

    def eval(self,id:str|None = None) -> str:
        ...
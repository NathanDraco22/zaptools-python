from typing import Protocol, Any

class ConnectionAdapter(Protocol):

    websocket:Any

    def __init__(self, websocket) -> None:
        self.websocket = websocket

    async def start_connection(self):
        ...

    async def recv_json(self) -> dict[str, Any]:
        ...
    
    async def send_event(self, event_name:str, payload:dict[str, Any]):
        ...
    
    async def close(self):
        ...


class IDController(Protocol):
    _ID_HEADING = "zpt"

    def eval(self,id:str|None = None) -> str:
        ...
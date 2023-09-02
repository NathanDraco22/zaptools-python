from typing import Protocol, Coroutine, Any, Callable

class ZapClient(Protocol):
    id:str
    async def send_event(self, event_name:str, payload: Any) -> Coroutine:
        ...
    async def close_conection(self) -> Coroutine:
        ...

class ZapEvent(Protocol):
    name:str
    payload:Any

class ZapContext(Protocol):
    event:ZapEvent
    client:ZapClient
    event_name:str
    payload:Any   
    client_id:str 


CallBackContext = Callable[[ZapContext], Coroutine]
CallBackClient = Callable[[ZapClient], Coroutine]

class ZapRegister(Protocol):
    def on_connected(self, callback: CallBackContext):
        ...
    
    def on_disconnected(self, callback: CallBackContext):
        ...
    
    def on_event(self, name:str):
        ...

class IDManager(Protocol):

    def process_id(id: str|None) -> str:
        ...

class ConnectionIndentifier(Protocol):
    is_new :bool
    connection_id :str 
    event: ZapEvent

class ConnectionVerifier(Protocol):
    def check_is_new_connection(cls,data:Any)->bool:
        ...
    
    def process_init_connection(cls, data:dict) -> ConnectionIndentifier:
        ...
    
    def process_end_connection(cls, indentifier: ConnectionIndentifier):
        ...
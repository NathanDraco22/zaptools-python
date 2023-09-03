from typing import Protocol, Coroutine, Any, Callable

class ZapWebSocketConnection(Protocol):
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
    client:ZapWebSocketConnection
    event_name:str
    payload:Any   
    client_id:str 


CallBackContext = Callable[[ZapContext], Coroutine]
CallBackClient = Callable[[ZapWebSocketConnection], Coroutine]

class ZapRegister(Protocol):
    def on_connected(self, callback: CallBackContext):
        ...
    
    def on_disconnected(self, callback: CallBackContext):
        ...
    
    def on_event(self, name:str):
        ...


class ZapEventCaller(Protocol):
    def add_register(self, register: ZapRegister):
        ...
    
    async def trigger_on_connected(self, ctx: ZapContext):
        ...
    
    async def trigger_on_disconnected(self, client: ZapContext):
        ...

    async def trigger_event(self, ctx: ZapContext):
        ...

class ZapEventBook:
    events: dict[str,CallBackContext]

    on_connected_event: CallBackContext|None= None
    on_disconnected_event: CallBackContext|None= None

    def regis_event(self, name:str, callback:CallBackContext):
        ...
    
    def del_event(self, name:str):
        ...
    
    def get_callable(self, name:str) -> CallBackContext|None:
        ...
    

class IDManager(Protocol):

    def process_id(id: str|None) -> str:
        ...

class ZapConnectionIndentifier(Protocol):
    is_new :bool
    connection_id :str 
    event: ZapEvent

class ZapConnectionVerifier(Protocol):
    def check_is_new_connection(cls,data:Any)->bool:
        ...
    
    def process_init_connection(cls, data:dict) -> ZapConnectionIndentifier:
        ...
    
    def process_end_connection(cls, indentifier: ZapConnectionIndentifier):
        ...
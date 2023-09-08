from typing import Protocol, Coroutine, Any, Callable

class ConnectionWrapper(Protocol):
    websocket: Any

    def __init__(self, websocket) -> None:
        self.websocket = websocket
        
    async def send_event(self, event_name:str, payload: Any) -> Coroutine:
        ...
    async def close_conection(self) -> Coroutine:
        ...

class WebSocketConnection(Protocol):
    id:str
    _wrapper : ConnectionWrapper

    async def send_event(self, event_name:str, payload: Any) -> Coroutine:
        await self._wrapper.send_event(event_name, payload)
    async def close(self) -> Coroutine:
        await self._wrapper.close_conection()

class Event(Protocol):
    name:str
    payload:Any


class EventContext(Protocol):
    event:Event
    connection:WebSocketConnection
    event_name:str
    payload:Any   
    connection_id:str 

class ConnectionIndentifier(Protocol):
    is_new : bool
    connection_id : str
    event : Event

CallBackContext = Callable[[EventContext], Coroutine]
CallBackClient = Callable[[WebSocketConnection], Coroutine]

class ZapEventRegister(Protocol):
    def on_connected(self, callback: CallBackContext):
        ...
    
    def on_disconnected(self, callback: CallBackContext):
        ...
    
    def on_event(self, name:str):
        ...


class ZapEventCaller(Protocol):
    def add_register(self, register: ZapEventRegister):
        ...
    
    async def trigger_on_connected(self, ctx: EventContext):
        ...
    
    async def trigger_on_disconnected(self, client: EventContext):
        ...

    async def trigger_event(self, ctx: EventContext):
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
    event: Event

class ZapConnectionVerifier(Protocol):
    def check_is_new_connection(cls,data:Any)->bool:
        ...
    
    def process_init_connection(cls, data:dict) -> ZapConnectionIndentifier:
        ...
    
    def process_end_connection(cls, indentifier: ZapConnectionIndentifier):
        ...
    
class ZapConnectionAuditor(IDManager, ZapConnectionVerifier, Protocol):
    ...
from typing import Any
from .protocols import (
    ZapWebSocketConnection, 
    ZapEvent, 
    ZapContext, 
    ZapEventRegister, 
    CallBackContext, 
    ZapEventCaller
)


class Context(ZapContext):
    def __init__(self, event: ZapEvent, client: ZapWebSocketConnection) -> None:
        self.event: ZapEvent = event
        self.client: ZapWebSocketConnection = client
        self.event_name = event.name
        self.payload    = event.payload
        self.client_id  = client.id
        pass    


class Event(ZapEvent):
    def __init__(self, name:str, payload:Any) -> None:
        self.name: str = name
        self.payload: Any = payload
        pass

class EventBook:
    events: dict[str,CallBackContext]

    def __init__(self) -> None:
        self.events = {}

    on_connected_event: CallBackContext|None= None
    on_disconnected_event: CallBackContext|None= None

    def regis_event(self, name:str, callback:CallBackContext):
        self.events[name] = callback 
    
    def del_event(self, name:str):
        self.events.pop(name)
    
    def get_callable(self, name:str) -> CallBackContext|None:
        stored_callable = self.events.get(name) 
        return stored_callable
    
class EventRegister(ZapEventRegister):
    _event_book : EventBook
    def __init__(self, event_book = EventBook()) -> None:
        self._event_book = event_book
        pass

    def on_connected(self, callback: CallBackContext):
        def wrapper(callback: CallBackContext):
            self._event_book.on_connected_event = callback
        wrapper(callback)
        return None
    
    def on_disconnected(self, callback: CallBackContext):
        def wrapper(callback: CallBackContext):
            self._event_book.on_disconnected_event = callback
        wrapper(callback)
        return
    
    def on_event(self, name:str):
        def wrapper(cb: CallBackContext):
            self._event_book.regis_event(name, cb)
        return wrapper


class EventCaller(ZapEventCaller):

    def add_register(self, register: EventRegister):
        self._register = register._event_book
    
    async def trigger_on_connected(self, ctx: Context):
        await self._register.on_connected_event(ctx)
    
    async def trigger_on_disconnected(self, client: Context):
        if not self._register.on_disconnected_event: 
            return
        await self._register.on_disconnected_event(client)

    async def trigger_event(self, ctx: Context):
        event = ctx.event
        result = self._register.get_callable(event.name)
        if not result: 
            return
        await result(ctx)

class Room:
    id:str
    clients : list[ZapWebSocketConnection] = []
    _private_client: ZapWebSocketConnection|None

    def __init__(self, clients:list[ZapWebSocketConnection]) -> None:
        self.clients = clients
        if len(clients) == 1: 
            self._private_client = clients[0]
        pass
    async def notify(self, event_name:str, payload: Any):
        if not self._private_client:
            await self._private_client.send_event(event_name, payload)
            return
        for client in self.clients:
            await client.send_event(event_name, payload)

class RoomManager:
    pass
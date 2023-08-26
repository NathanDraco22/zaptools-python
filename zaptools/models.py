from typing import Callable, Any, Coroutine
from .protocols import WebSocketClient, WebSocketEvent


class Context:
    def __init__(self, event: WebSocketEvent, client: WebSocketClient) -> None:
        self.event: WebSocketEvent = event
        self.client: WebSocketClient = client
        pass    


class Event:
    def __init__(self, name:str, payload:dict) -> None:
        self.name: str = name
        self.payload: str = payload
        pass

CallBackContext = Callable[[Context], Coroutine]
CallBackClient = Callable[[WebSocketClient], Coroutine]

class EventBook:
    events: dict[str,CallBackContext] = {}

    on_connected_event: CallBackClient|None= None
    on_disconnected_event: Callable|None= None

    def regis_event(self, name:str, callback:CallBackContext):
        self.events[name] = callback 
    
    def del_event(self, name:str):
        self.events.pop(name)
    
    def get_callable(self, name:str) -> CallBackContext|None:
        stored_callable = self.events.get(name) 
        return stored_callable


class EventFactory:
    @staticmethod
    def from_dict(data: dict[str, Any]) -> Event:
        return Event(
            name= data["name"],
            payload= data["payload"]
        )
    
    @staticmethod
    def event_to_dict( event: Event ) -> dict[str, Any]:
        return vars(event)
    
class EventRegister:
    _event_book : EventBook
    def __init__(self) -> None:
        self._event_book = EventBook()
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


class WebSocketHandler:

    def add_register(self, register: EventRegister):
        self._register = register._event_book
    
    async def trigger_on_connected(self, client: WebSocketClient):
        await self._register.on_connected_event(client)
    
    async def trigger_on_disconnected(self):
        if not self._register.on_disconnected_event: return
        await self._register.on_disconnected_event()

    async def trigger_event(self, ctx: Context):
        event = ctx.event
        result = self._register.get_callable(event.name)
        if not result: return
        await result(ctx)


class Room:
    id:str
    clients : list[WebSocketClient] = []
    _private_client: WebSocketClient|None

    def __init__(self, clients:list[WebSocketClient]) -> None:
        self.clients = clients
        if len(clients) == 1: self._private_client = clients[0]
        pass
    async def notify(self, event_name:str, payload: Any):
        if self._private_client != None:
            await self._private_client.send_event(event_name, payload)
            return
        for client in self.clients:
            await client.send_event(event_name, payload)

class RoomManager:
    pass
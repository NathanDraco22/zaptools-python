import uuid
from typing import Callable, Any
from .protocols import ConnectionAdapter

class Event:
    def __init__(self, name:str, callback: Callable) -> None:
        self.name = name
        self.callback = callback

class WebSocketConnection:

    id:str

    _connection_adapter: ConnectionAdapter

    def __init__(self, id:str,connection_adapter: ConnectionAdapter) -> None:
        self._connection_adapter = connection_adapter
        self.id = id

    async def send(self, event_name: str, payload: dict[str, Any]):
        await self._connection_adapter.send_event(event_name,payload)
    
    async def close(self):
        await self._connection_adapter.close()


class Context:

    event_name:str
    payload: dict[str, Any]
    connection: WebSocketConnection

    def __init__(self, 
                 event_name:str, 
                 payload: dict[str, Any], 
                 connection: WebSocketConnection
    ) -> None:
        self.event_name = event_name
        self.payload = payload
        self.connection = connection

class IDController:
    _ID_HEADING = "zpt"

    def eval(self,id:str|None = None) -> str:
        if id: 
            return id
        return str(f"{self._ID_HEADING}-{uuid.uuid4()}")



#------------------------------------------------------------------------------

class EventBook:
    event_records: dict[str, Event] = {}

    def save_event(self, event: Event):
        self.event_records[event.name] = event

    def get_event(self, name:str) -> Event|None:
        return self.event_records.get(name)


class EventRegister:

    def __init__(self, event_book: EventBook = EventBook()) -> None:
        self._event_book = event_book
    
    def on_event(self,name: str):
        def inner(callback: Callable):
            event = Event(name, callback)
            self._event_book.save_event(event)
        return inner


class EventCaller:
    def __init__(self, event_register: EventRegister) -> None:
        self._event_book = event_register._event_book
        
    async def trigger_event(self, ctx: Context):
        event = self._event_book.get_event(ctx.event_name)
        if not event:
            return
        await event.callback(ctx)


# ----------------------------------------------------------------------------------


class EventProcessor:

    _connection: WebSocketConnection
    _event_caller: EventCaller
    _adapter: ConnectionAdapter

    def __init__(self, 
                 connection: WebSocketConnection, 
                 event_caller: EventCaller
    ) -> None:
        self._connection = connection
        self._event_caller = event_caller
        self._adapter = connection._connection_adapter

    async def notify_connected(self):
        EVENT_NAME = "connected"
        ctx = Context(EVENT_NAME, {}, self._connection)
        await self._event_caller.trigger_event(ctx)
    
    async def notify_disconnected(self):
        EVENT_NAME = "disconnected"
        ctx = Context(EVENT_NAME, {}, self._connection)
        await self._event_caller.trigger_event(ctx)
    
    async def receive_events(self):
        data = await self._adapter.recv_json()
        ctx = Context(data["eventName"], data["payload"], self._connection)
        await self._event_caller.trigger_event(ctx)
    
    async def intercept_data(self, data: dict[str,Any]):
        ctx = Context(data["eventName"], data["payload"], self._connection)
        await self._event_caller.trigger_event(ctx)
    
    async def start_event_stream(self):
        await self.notify_connected()
        try:
            while True:
                await self._adapter.recv_json()
        except Exception:
            await self.notify_disconnected()



class Connector:

    _adapter: ConnectionAdapter

    def __init__(self, 
                 register: EventRegister, 
                 adapter_type: type[ConnectionAdapter],
                 id_controller: IDController = IDController()
    ) -> None:
        self.register = register
        self.event_caller = EventCaller(register)
        self.adapter_type = adapter_type
        self.id_controller = id_controller
    
    async def plug(self, websocket) -> EventProcessor:
        self._adapter = self.adapter_type(websocket)
        await self._adapter.start_connection()
        current_id =self.id_controller.eval()
        ws_connection = WebSocketConnection(current_id,self._adapter)
        return EventProcessor(ws_connection, self.event_caller)
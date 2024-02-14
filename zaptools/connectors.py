from typing import Any
from .tools import (
    EventRegister, 
    EventCaller, 
    IDController, 
    WebSocketConnection,
    EventProcessor
)
from .adapters import FastApiAdapter, SanicAdapter

class FastApiConnector:

    def __init__(
            self, 
            register: EventRegister, 
            webscoket: Any, 
            connection_id:str|None=None
    ):
        self.register = register
        self.websocket = webscoket
        self._connection_id = connection_id

    async def start(self):
        fastapi_adapter = FastApiAdapter(self.websocket)
        event_caller = EventCaller(self.register._event_book)
        id_controller = IDController()
        await fastapi_adapter.start_connection()
        current_id = id_controller.eval(self._connection_id)
        ws_connection = WebSocketConnection(current_id, fastapi_adapter)
        event_processor = EventProcessor(ws_connection, event_caller)
        await event_processor.start_event_stream()


    @staticmethod
    async def plug(register: EventRegister, websocket: Any):
        fastapi_adapter = FastApiAdapter(websocket)
        event_caller = EventCaller(register._event_book)
        id_controller = IDController()
        await fastapi_adapter.start_connection()
        current_id = id_controller.eval()
        ws_connection = WebSocketConnection(current_id, fastapi_adapter)
        return EventProcessor(ws_connection, event_caller)
    
    @staticmethod
    async def plug_and_start(register: EventRegister, websocket: Any):
        fastapi_adapter = FastApiAdapter(websocket)
        event_caller = EventCaller(register._event_book)
        id_controller = IDController()
        await fastapi_adapter.start_connection()
        current_id = id_controller.eval()
        ws_connection = WebSocketConnection(current_id, fastapi_adapter)
        event_processor = EventProcessor(ws_connection, event_caller)
        await event_processor.start_event_stream()


class SanicConnector:

    def __init__(
            self, 
            register: EventRegister, 
            webscoket: Any,
            connection_id:str|None=None
    ):
        self.register = register
        self.websocket = webscoket
        self.connection_id = connection_id

    async def start(self):
        sanic_adapter = SanicAdapter(self.websocket)
        event_caller = EventCaller(self.register._event_book)
        id_controller = IDController()
        await sanic_adapter.start_connection()
        current_id = id_controller.eval(self.connection_id)
        ws_connection = WebSocketConnection(current_id, sanic_adapter)
        event_processor =  EventProcessor(ws_connection, event_caller)
        await event_processor.start_event_stream()

    @staticmethod
    async def plug(register: EventRegister, websocket: Any):
        fastapi_adapter = SanicAdapter(websocket)
        event_caller = EventCaller(register._event_book)
        id_controller = IDController()
        await fastapi_adapter.start_connection()
        current_id = id_controller.eval()
        ws_connection = WebSocketConnection(current_id, fastapi_adapter)
        return EventProcessor(ws_connection, event_caller)
    
    @staticmethod
    async def plug_and_start(register: EventRegister, websocket: Any):
        fastapi_adapter = SanicAdapter(websocket)
        event_caller = EventCaller(register._event_book)
        id_controller = IDController()
        await fastapi_adapter.start_connection()
        current_id = id_controller.eval()
        ws_connection = WebSocketConnection(current_id, fastapi_adapter)
        event_processor =  EventProcessor(ws_connection, event_caller)
        await event_processor.start_event_stream()
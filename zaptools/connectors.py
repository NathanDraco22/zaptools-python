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
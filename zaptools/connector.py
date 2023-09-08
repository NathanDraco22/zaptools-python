import json
from typing import Any

from .protocols import (
    ZapEventRegister
)
from .helpers import ZaptoolHelper, ConnectionIndentifier
from .tools import EventCaller, Context, ConnectionWrapper
from .factories import Event, EventFactory

class MyWrapper():
    def __init__(self, websocket) -> None:
        self.wsc = websocket

    async def send_event(self, event_name:str, payload: Any):
        print("llega")
        new_event = Event(event_name, payload)
        event_dict = EventFactory.event_to_dict(new_event)
        data = json.dumps(event_dict, indent=4)
        await self.wsc.send_json(data, mode="binary")

    async def close_conection(self):
        await self.wsc.close()

class ZapToolConnector:

    def __init__(self, 
        register: ZapEventRegister,
    ) -> None:
        self.register = register
        self.event_caller = EventCaller(register)
        self.zap_helper = ZaptoolHelper()
        pass

    def verify_init_data(self,data: Any, ws) -> (EventCaller, Context):
        conn_wrapper = MyWrapper(ws)
        identifier = self.zap_helper.process_init_connection(data)
        self.event_caller = EventCaller(self.register)
        ctx = Context(conn_wrapper, identifier)
        return (self.event_caller, ctx)
    
    async def process_loop_data(self, ctx: Context, data):
         event = EventFactory.from_dict(data)
         loop_identifier = self.zap_helper.proccess_loop_connection(
                        ctx.conn_identifier, 
                        event
                    )
         ctx = Context(ctx.conn_wrapper, loop_identifier)
         await self.event_caller.trigger_event(ctx)

class ZaptoolEventManager:
    register: ZapEventRegister
    event_caller: EventCaller
    zap_helper: ZaptoolHelper
    _wrapper : ConnectionWrapper

    def __init__(self, register: ZapEventRegister) -> None:
        self.register = register
        self.event_caller = EventCaller(register)
        self.zap_helper = ZaptoolHelper()

    def wrap_connection(self,websocket, wrapper: type[ConnectionWrapper]):
        self._wrapper = wrapper(websocket)
    
    async def process_events(self, data):
        event = EventFactory.from_dict(data)
        connection_id = self.zap_helper.process_id()
        conn_identifier = ConnectionIndentifier(True,connection_id, event)
        ctx = Context(self._wrapper, conn_identifier)
        await self.event_caller.trigger_event(ctx)


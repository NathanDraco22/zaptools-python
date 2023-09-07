import json
from typing import Any

from .protocols import (
    ZapEventRegister
)
from .helpers import ZaptoolHelper
from .tools import EventCaller, Context
from .factories import Event, EventFactory

class MyWrapper():
    def __init__(self, websocket) -> None:
        self.wsc = websocket

    async def send_event(self, event_name:str, payload: Any):
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
        self.event_caller = EventCaller()
        self.zap_helper = ZaptoolHelper()
        pass

    def verify_init_data(self,data: Any, ws) -> (EventCaller, Context):
        conn_wrapper = MyWrapper(ws)
        identifier = self.zap_helper.process_init_connection(data)
        self.event_caller = EventCaller()
        self.event_caller.add_register(self.register)
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
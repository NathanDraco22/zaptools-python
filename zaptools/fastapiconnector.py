import json
from typing import Any
from fastapi import WebSocket

from .tools import EventCaller, Event, Context
from .factories import EventFactory
from .helpers import ZaptoolHelper

class MyWrapper():
    def __init__(self, websocket : WebSocket) -> None:
        self.wsc = websocket

    async def send_event(self, event_name:str, payload: Any):
        new_event = Event(event_name, payload)
        event_dict = EventFactory.event_to_dict(new_event)
        data = json.dumps(event_dict, indent=4)
        await self.wsc.send_json(data, mode="binary")

    async def close_conection(self):
        await self.wsc.close()

class FastApiConnector:

    @classmethod
    def start(cls,app, register , path:str= "/" ):
       
        zap_helper = ZaptoolHelper()
        @app.websocket(path)
        async def endpoint(ws: WebSocket):
            await ws.accept()
            conn_wrapper = MyWrapper(ws)
            data = await ws.receive_json()
            identifier = zap_helper.process_init_connection(data)
            event_caller = EventCaller()
            event_caller.add_register(register)
            ctx = Context(conn_wrapper, identifier)
            await event_caller.trigger_on_connected(ctx)
            try: 
                while True:
                    data = await ws.receive_json()
                    event = EventFactory.from_dict(data)
                    loop_identifier = zap_helper.proccess_loop_connection(
                        identifier, 
                        event
                    )
                    ctx = Context(conn_wrapper, loop_identifier)
                    await event_caller.trigger_event(ctx)
            except Exception:
                end_indentifier = zap_helper.process_end_connection(identifier)
                ctx = Context(conn_wrapper, end_indentifier)
                await event_caller.trigger_on_disconnected(ctx)

import json
from typing import Any
from fastapi import WebSocket

from .tools import Event, Context, EventRegister
from .factories import EventFactory
from .helpers import ZaptoolHelper
from .connector import ZapToolConnector

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
    def start(cls,app, register: EventRegister , path:str= "/" ):
        zaptool_connector = ZapToolConnector(register)
        zap_helper = ZaptoolHelper()
        @app.websocket(path)
        async def endpoint(ws: WebSocket):
            await ws.accept()
            data = await ws.receive_json()
            event_caller, ctx = zaptool_connector.verify_init_data(data, ws)
            identifier = ctx.conn_identifier
            await event_caller.trigger_on_connected(ctx)
            try: 
                while True:
                    data = await ws.receive_json()
                    await zaptool_connector.process_loop_data(ctx, data)
            except Exception as e:
                print(e)
                end_indentifier = zap_helper.process_end_connection(identifier)
                ctx = Context(ctx.conn_wrapper, end_indentifier)
                await event_caller.trigger_on_disconnected(ctx)

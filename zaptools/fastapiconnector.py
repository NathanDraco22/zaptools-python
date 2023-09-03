from fastapi import WebSocket

from .wrappers import FastApiWSConn
from .tools import EventCaller, Context
from .factories import EventFactory
from .helpers import ZaptoolHelper

class FastApiConnector:

    @classmethod
    def start(cls,app, register, path:str= "/" ):
        zap_helper = ZaptoolHelper()
        @app.websocket(path)
        async def endpoint(ws: WebSocket):
            await ws.accept()
            data = await ws.receive_json()
            identifier = zap_helper.process_init_connection(data)
            client_fast = FastApiWSConn(ws, identifier.connection_id)
            event_caller = EventCaller()
            event_caller.add_register(register)
            ctx = Context(identifier.event, client_fast)
            await event_caller.trigger_on_connected(ctx)
            try: 
                while True:
                    data = await ws.receive_json()
                    event = EventFactory.from_dict(data)
                    ctx = Context(event= event, client= client_fast)
                    await event_caller.trigger_event(ctx)
            except Exception:
                end_indentifier = zap_helper.process_end_connection(identifier)
                ctx = Context(end_indentifier.event, client_fast)
                await event_caller.trigger_on_disconnected(ctx)

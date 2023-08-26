from fastapi import WebSocket

from .wrappers import FastApiWSWrapper
from .models import WebSocketHandler, EventFactory, Context

class FastApiConnector:

    @classmethod
    def start(cls,app, register, path:str= "/" ):
        @app.websocket(path)
        async def endpoint(ws: WebSocket):
            await ws.accept()
            print(ws.client)
            client_fast = FastApiWSWrapper(ws)
            ws_handler = WebSocketHandler()
            ws_handler.add_register(register)
            await ws_handler.trigger_on_connected(client_fast)
            try: 
                while True:
                    data = await ws.receive_json()
                    event = EventFactory.from_dict(data)
                    ctx = Context(event= event, client= client_fast)
                    await ws_handler.trigger_event(ctx)
            except Exception as e:
                print(e)
                await ws_handler.trigger_on_disconnected()

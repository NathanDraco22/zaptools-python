from typing import Coroutine, List
from fastapi import FastAPI

#================= THIS IS ONLY FOR DEV HELPERS ===================================

class FastApiZapAdapter():

    app : FastAPI
    _socket_events : List

    def _add_client_connected(self, socket_client) -> Coroutine:
        pass
    def _remove_client_disconnected(self, socket_client) -> Coroutine:
        pass

    async def _on_any_event_recieved(self, zap_data_model ,socket_client) -> Coroutine:
        pass
#==================================================================================
class SocketClient():
    id_connection : str
    async def send_event(self, event:str ,payload : any):
        pass
#==================================================================================
class Payload():
    pass

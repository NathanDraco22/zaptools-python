from fastapi import FastAPI, WebSocket
from typing import Callable, Coroutine, List

from zaptools.EventRegister.EventRegister import EventRegister
from zaptools.FastApi.FastApiAdapter import FastApiWebSocketAdapter
from zaptools.customtypes.types import SocketClient, FastApiZapAdapter
from zaptools.models.ZapDataModel import ZapDataModel
from zaptools.models.socket_event_model import SocketEvent

class AdapterEvent():

    callback : Callable[[SocketClient ,  FastApiZapAdapter], Coroutine]

    def __init__(self, 
    callback : Callable[[SocketClient ,  FastApiZapAdapter], Coroutine]) -> None:
        self.callback = callback

#===============================================================================================

class FastApiZapAdapter():

    app: FastAPI

    _socket_events : List[SocketEvent]  = []
    _route: str
    _adapter : FastApiWebSocketAdapter

    _clients_connected : List[SocketClient] = []

    _on_connected_event    : AdapterEvent
    _on_disconnected_event : AdapterEvent
    _on_any_event          : SocketEvent

    def __init__(self,app: FastAPI, route:str  ="/" ) -> None:

        self.app = app
        self._route = route
        self._socket_events = []
        self._on_connected_event    : AdapterEvent = None
        self._on_disconnected_event : AdapterEvent = None
        self._on_any_event          : SocketEvent = None

        @self.app.websocket(route)
        async def websocket( ws : WebSocket ):
            adapter = FastApiWebSocketAdapter(
                websocket= ws,
                ws_events= self._socket_events,
                zap_tool= self
            )
            #-- init adapter --
            await adapter.init_adapter()

#--------------------------------------------------------------------------------------------  
   
    def on_event(self,event:str):

        def internal(my_func):
            my_func : Callable[[], Coroutine]
            socket_event = SocketEvent(event, my_func)
            self._socket_events.append(socket_event)
        return internal
    
    def on_client_connected(self, my_func):
        def internal(my_func):
            my_func : Callable[[], Coroutine]
            socket_event = AdapterEvent(my_func)
            self._on_connected_event = socket_event
        internal(my_func)
        return None

    def on_any_event(self, my_func):
        def internal(my_func):
            my_func : Callable[[], Coroutine]
            socket_event = AdapterEvent(my_func)
            self._on_any_event = socket_event
        internal(my_func)
        return None
    
    def on_client_disconnected(self, my_func):
        def internal(my_func):
            my_func : Callable[[], Coroutine]
            adapter_event  = AdapterEvent(my_func)
            self._on_disconnected_event = adapter_event
        internal(my_func)   
        return None
    
    def add_events_from_register(self ,register : EventRegister):
        event_registered = register.get_events()
        self._socket_events = [ *self._socket_events , *event_registered ]
    
    async def send_all_clients(self,event : str , payload ):
        for client in self._clients_connected:
            await client.send_event(event , payload)
            
#--------------------------------------------------------------------------------------------
    async def _add_client_connected(self, socket_client : SocketClient):
        self._clients_connected.append(socket_client)
        if self._on_connected_event != None:
            await self._on_connected_event.callback(socket_client , self )
    
    async def _remove_client_disconnected(self, socket_client : SocketClient):
        self._clients_connected.remove(socket_client)
        if self._on_disconnected_event != None:
            await self._on_disconnected_event.callback(socket_client,self)
    
    async def _on_any_event_recieved(self, zap_data_model : ZapDataModel ,socket_client :SocketClient):
        payload : any = zap_data_model.payload
        if self._on_any_event != None:
            await self._on_any_event.callback(payload , socket_client , self)
          
#==================================================================================
#                                  TYPES
# ==================================================================================
class SocketClient():
    id_connection : str
    async def send_event(self, event:str ,payload : any):
        pass




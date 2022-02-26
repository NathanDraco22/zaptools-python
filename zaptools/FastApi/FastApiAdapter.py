from typing import Callable, Coroutine, List
from fastapi import WebSocket
from uuid import uuid4

from zaptools.models.SendingModel import SendingModel
from zaptools.models.ZapDataModel import ZapDataModel

from zaptools.models.socket_event_model import SocketEvent, FastApiZapAdapter, SocketClient

class SocketClient():

    _websocket : WebSocket
    id_connection : str

    def __init__(self, websocket: WebSocket, id_conection:str) -> None:
        self._websocket = websocket
        self.id_connection = id_conection
        pass

    async def send_event(self, event:str ,payload : any):
        client_id = self.id_connection
        socket_message = ZapDataModel(client_id, "FastApi", event, payload)
        await self._websocket.send_json( socket_message.toJsonDict() )

#================================================================================================

class FastApiWebSocketAdapter():

    websocket: WebSocket
    __is_connected : bool = False

    ws_events : List[SocketEvent] = []

    _send_request : List[SocketEvent] = []
    _zap_tool : FastApiZapAdapter

    def __init__(self, 
    websocket : WebSocket, 
    ws_events : List[SocketEvent],
    zap_tool : FastApiZapAdapter
    ) -> None:
        self.websocket = websocket
        self.ws_events = ws_events
        self._zap_tool = zap_tool
        pass

#----------------------------------------------------------------------------------------
    async def init_adapter(self):
        #---------- INIT PROTOCOL --------------
        await self.websocket.accept()
        unique_id: str = "zp+" + str(uuid4())
        init_message = SendingModel(unique_id, "FastApi", "zap+nat-v1::aqua_indigo::", "connecting to FastApi web socket, use ZapTool package")
        await self.websocket.send_json(init_message.toJsonDict())
        confirm_data = await self.websocket.receive_json()
        
        client_socket: SocketClient

        try:
            confirmed = ZapDataModel.fromJsonDict(confirm_data)

            print(confirmed.payload)

            client_socket = SocketClient(self.websocket, id_conection= unique_id)

            self.__is_connected = True
        except:
            self.__is_connected = False
            return
        
        #----------- LOOP-CORE -------------

        #-- trigger on connect --
        await self._zap_tool._add_client_connected(client_socket)

        try:
            while self.__is_connected:
                data      = await self.websocket.receive_json()
                zap_model = ZapDataModel.fromJsonDict( data )
                #-- event trigger --
                await self.dispatch_events( zap_model , client_socket, self._zap_tool )
                await self._zap_tool._on_any_event_recieved(zap_model , client_socket)
        except:
            pass

        #-- trigger on disconnect --
        await self._zap_tool._remove_client_disconnected(client_socket)
        
        
    async def dispatch_events(self, 
    zap_model : ZapDataModel, 
    client_socket : SocketClient,
    zap_tool: FastApiZapAdapter
    ):
        event_name = zap_model.event
        s_events = zap_tool._socket_events

        for s_event in s_events:
            if (event_name == s_event.event_name):
                s_event : SocketEvent
                await s_event.callback(zap_model.payload, client_socket, zap_tool)
    

    def on_event(self,event_name : str , callback: Callable[ [any, SocketClient, FastApiZapAdapter], Coroutine ]):
        socket_event = SocketEvent(event_name= event_name , callback= callback)
        self.ws_events.append( socket_event )









import uuid
from typing import Any

from .tools import Event
from .protocols import ZapConnectionAuditor

class ConnectionIndentifier:
    def __init__(self, is_new:bool, connection_id:str, event: Event ) -> None:
        self.is_new :bool = is_new
        self.connection_id :str = connection_id
        self.event = event
        pass

class ZaptoolHelper(ZapConnectionAuditor):
    
    _INIT_EVENT_NAME = "init"
    _END_EVENT_NAME = "end"
    _ID_HEADING = "zpt"

    
    def process_id(self,id:str|None) -> str:
        if id: 
            return id
        return str(f"{self._ID_HEADING}-{uuid.uuid4()}")
    
    
    def check_is_new_connection(self,data:Any)->bool:
        event_name = data["name"]
        event_payload: dict = data['payload']
        conection_id = event_payload.get("id")
        return conection_id is None and event_name == self._INIT_EVENT_NAME
    
    
    def process_init_connection(self, data:dict) -> ConnectionIndentifier:
        is_new_connection = self.check_is_new_connection(data)
        payload_id = data.get("payload").get("id")
        connection_id = self.process_id(payload_id)
        init_event = Event(self._INIT_EVENT_NAME, data["payload"])
        return ConnectionIndentifier(is_new_connection, connection_id, init_event)
    
    
    def process_end_connection(self, indentifier: ConnectionIndentifier):
        event = Event(self._END_EVENT_NAME, {})
        return ConnectionIndentifier(
            indentifier.is_new, 
            indentifier.connection_id, 
            event
        )




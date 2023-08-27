import uuid
from typing import Any

from .models import Event

class ConnectionIndentifier:
    def __init__(self, is_new:bool, connection_id:str, event: Event ) -> None:
        self.is_new :bool = is_new
        self.connection_id :str = connection_id
        self.event = event
        pass

class ZaptoolHelper:
    
    _INIT_EVENT_NAME = "init"
    _END_EVENT_NAME = "end"
    _ID_HEADING = "zpt"

    @classmethod
    def process_id(cls,id:str|None) -> str:
        if id: 
            return id
        return str(f"{cls._ID_HEADING}-{uuid.uuid4()}")
    
    @classmethod
    def check_is_new_connection(cls,data:Any)->bool:
        event_name = data["name"]
        event_payload: dict = data['payload']
        conection_id = event_payload.get("id")
        return conection_id is None and event_name == cls._INIT_EVENT_NAME
    
    @classmethod
    def process_init_connection(cls, data:dict) -> ConnectionIndentifier:
        print(data)
        is_new_connection = cls.check_is_new_connection(data)
        payload_id = data.get("payload").get("id")
        connection_id = cls.process_id(payload_id)
        print(connection_id)
        init_event = Event(cls._INIT_EVENT_NAME, data["payload"])
        return ConnectionIndentifier(is_new_connection, connection_id, init_event)
    
    @classmethod
    def process_end_connection(cls, indentifier: ConnectionIndentifier):
        event = Event(cls._END_EVENT_NAME, {})
        return ConnectionIndentifier(
            indentifier.is_new, 
            indentifier.connection_id, 
            event
        )




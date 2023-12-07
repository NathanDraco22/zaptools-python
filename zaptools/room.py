import asyncio
from .tools import WebSocketConnection
from typing import Any
from .meta_tag import MetaTag

class Room:

    name: str
    _connections: dict[str, WebSocketConnection] = {}
    _meta: dict[str, Any] = {}
    
    def __init__(self, name:str):
        self.name = name

    def add(self,connection: WebSocketConnection, 
            meta_tag:MetaTag|None = None,
    ):
        self._connections[connection.id] = connection
        if meta_tag is None: 
            return
        self._meta[connection.id] = meta_tag
    
    def get_meta(self, connection: WebSocketConnection)-> MetaTag:
        return self._meta.get(connection.id)

    def remove(self, connection: WebSocketConnection):
        del self._connections[connection.id]
    
    async def send(
            self,
            event_name:str, 
            payload: Any, 
            headers: dict|None = None,
            exclude: WebSocketConnection|None = None
        ):
        coros = [
            conn.send()
            for _,conn in self._connections.items() 
            if exclude is not None and exclude.id == conn.id
        ]
        await asyncio.gather(*coros)


class RoomManager:

    _room_book: dict[str, Room] = {}

    def add_room(self, room: Room):
        self._room_book[room.name] = room

    def remove_room(self, room: Room):
        del self._room_book[room.name]
    
    async def send_to_room(self, 
                     room_name: str,
                     event_name: str,
                     payload: Any,
                     headers: dict|None
    ):
        room = self._room_book.get(room_name)
        if room is None:
            return
        await room.send(event_name, payload, headers)
    
    def add_to_room(self, room_name: str, connection: WebSocketConnection):
        room = self._room_book.get(room_name)
        if(room_name is None):
            new_room = Room(room_name)
            new_room.add(connection)
            self._room_book[new_room.name] = new_room
            return
        room.add(connection)




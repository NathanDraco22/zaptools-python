import asyncio
from asyncio import Task
from .tools import WebSocketConnection
from typing import Any

class Room:

    name: str
    _connections: dict[str, WebSocketConnection] = {}
    
    def __init__(self, name:str):
        self.name = name

    def add(self,connection: WebSocketConnection):
        self._connections[connection.id] = connection

    def remove(self, connection: WebSocketConnection):
        del self._connections[connection.id]
    
    async def send(
            self,
            event_name:str, 
            payload: Any, 
            headers: dict|None = None,
            exclude: WebSocketConnection|None = None
        ):
        coros = []
        for _, conn in self._connections.items():
            if (exclude is not None and exclude.id == conn.id):
                continue
            coros.append(conn.send(event_name, payload,headers))
        asyncio.gather(*coros)


class RoomManager:

    _room_book: dict[str, Room] = {}

    def add_room(self, room: Room):
        self._room_book[room.name] = room

    def remove_room(self, room: Room):
        del self._room_book[room.name]
    
    def send_to_room(self, 
                     room_name: str,
                     event_name: str,
                     payload: Any,
                     headers: dict|None
    ) -> Task[None]:
        room = self._room_book.get(room_name)
        if room is None:
            return
        return room.send(event_name, payload, headers)
    
    def add_to_room(self, room_name: str, connection: WebSocketConnection):
        room = self._room_book.get(room_name)
        if(room_name is None):
            new_room = Room(room_name)
            new_room.add(connection)
            self._room_book[new_room.name] = new_room
            return
        room.add(connection)




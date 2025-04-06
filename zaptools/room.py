import asyncio
from .tools import WebSocketConnection
from typing import Any
from .meta_tag import MetaTag


class Room:

    name: str
    _connections: dict[str, WebSocketConnection] = {}
    _meta: dict[str, Any] = {}

    def __init__(self, name: str) -> None:
        self.name = name

    def add(
        self,
        connection: WebSocketConnection,
        meta_tag: MetaTag | None = None,
    ) -> None:
        self._connections[connection.id] = connection

        if meta_tag is None:
            return

        self._meta[connection.id] = meta_tag

    def get_meta(self, connection: WebSocketConnection) -> MetaTag | None:
        return self._meta.get(connection.id)

    def remove(self, connection: WebSocketConnection) -> None:
        del self._connections[connection.id]

    async def send(
        self,
        event_name: str,
        payload: Any,
        headers: dict[str, Any] | None = None,
        exclude: WebSocketConnection | None = None,
    ) -> None:
        wconnections = self._connections.values()
        exclude_id = "===" if exclude is None else exclude.id

        coros = [
            coro.send(event_name, payload, headers)
            for coro in wconnections
            if coro.id != exclude_id
        ]

        await asyncio.gather(*coros)


class RoomManager:
    _room_book: dict[str, Room] = {}

    def add_room(self, room: Room) -> None:
        self._room_book[room.name] = room

    def remove_room(self, room: Room) -> None:
        del self._room_book[room.name]

    async def send_to_room(
        self,
        room_name: str,
        event_name: str,
        payload: Any,
        headers: dict[str, Any] | None,
    ) -> None:
        room = self._room_book.get(room_name)

        if room is None:
            return

        await room.send(event_name, payload, headers)

    def add_to_room(self, room_name: str, connection: WebSocketConnection) -> None:
        room = self._room_book.get(room_name)

        if room is None:
            new_room = Room(room_name)
            new_room.add(connection)
            self._room_book[new_room.name] = new_room
            return

        room.add(connection)

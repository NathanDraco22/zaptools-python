import asyncio
from typing import Any, Coroutine
from zaptools.core import WebSocketConnection
from zaptools.zap_logger import zap_logger


class ConnectionRouter:
    """
    The ConnectionRouter class manages a collection of WebSocket connections,
    allowing you to add, remove, retrieve, and broadcast events to these connections.
    """

    def __init__(self) -> None:
        self._connections: dict[str, WebSocketConnection] = {}

    def add_connection(self, connection: WebSocketConnection) -> None:
        """
        Adds a WebSocket connection to the router.
        """
        self._connections[connection.id] = connection

    def remove_connection(self, connection: WebSocketConnection) -> None:
        """
        Removes a WebSocket connection from the router.
        """
        self._connections.pop(connection.id)

    def get_connection(self, id: str) -> WebSocketConnection | None:
        """
        Retrieves a WebSocket connection by its ID.
        """

        return self._connections.get(id)

    def get_all_connections(self) -> list[WebSocketConnection]:
        """
        Retrieves all the WebSocket connections in the router.

        Returns
            A list of WebSocketConnection objects.
        """
        return list(self._connections.values())

    async def broadcast(
        self,
        event_name: str,
        payload: Any = None,
        headers: dict[str, Any] | None = None,
        exclude: list[WebSocketConnection] | None = None,
    ) -> None:
        """
        Broadcasts an event to all the WebSocket connections in the router.

        Args:
            event_name (str): The name of the event to broadcast.
            payload (dict[str, Any], optional): The payload of the event. Defaults to {}.
            headers (dict[str, Any] | None, optional): The headers of the event. Defaults to None.
            exclude (list[WebSocketConnection] | None, optional): A list of connections to exclude from the broadcast. Defaults to None.
        """

        coros: list[Coroutine] = []

        for connection in self.get_all_connections():
            if exclude and connection in exclude:
                continue

            coro = self.send_to_connection(
                connection.id,
                event_name,
                payload,
                headers,
            )
            coros.append(coro)

        await asyncio.gather(*coros)
        return

    async def send_to_connection(
        self,
        connection_id: str,
        event_name: str,
        payload: dict[str, Any] = {},
        headers: dict[str, Any] | None = None,
    ) -> bool:
        """
        Sends an event to a WebSocket connection by its ID.
        returns True if the event was successfully sent, False otherwise

        Args:
            connection_id (str): The ID of the connection to send the event to.
            event_name (str): The name of the event to send.
            payload (dict[str, Any], optional): The payload of the event. Defaults to {}.
            headers (dict[str, Any] | None, optional): The headers of the event. Defaults to None.

        Returns:
            bool: True if the event was successfully sent, False otherwise.
        """
        connection = self.get_connection(connection_id)
        if connection is not None:
            try:
                await connection.send(event_name, payload, headers)
                return True
            except Exception:
                zap_logger.error(f"Error sending event to connection: {connection_id}")
                return False
        return False

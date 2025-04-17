from typing import Any
from zaptools.protocols import ConnectionAdapter


class WebSocketConnection:
    id: str

    _connection_adapter: ConnectionAdapter

    def __init__(self, id: str, connection_adapter: ConnectionAdapter) -> None:
        self._connection_adapter = connection_adapter
        self.id = id

    async def send(
        self,
        event_name: str,
        payload: Any,
        headers: dict[str, Any] | None = None,
    ) -> None:
        await self._connection_adapter.send_event(
            event_name,
            payload,
            headers,
        )

    async def close(self) -> None:
        await self._connection_adapter.close()

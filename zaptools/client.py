import enum
import json
import asyncio
from typing import Any, AsyncGenerator
from websockets.asyncio.client import connect

from .core.events import EventData
from .zap_logger import zap_logger


class ZapClientState(enum.Enum):
    ONLINE = 1
    OFFLINE = 2
    CONNECTING = 3
    ERROR = 4


class ZapClient:

    _connection_state_queue = asyncio.Queue[ZapClientState]()
    _current_state = ZapClientState.OFFLINE

    async def connect(self, url: str) -> None:
        await self._update_connection_state(ZapClientState.CONNECTING)
        self._conn = await connect(url)
        await self._update_connection_state(ZapClientState.ONLINE)
        zap_logger.info_green(f"Connected to {url}")

    async def send(
        self,
        event_name: str,
        payload: dict[str, Any],
        headers: dict[str, Any] | None = None,
    ) -> None:
        conn = self._conn
        inner_header = headers if headers is not None else {}
        event_data = EventData(event_name, payload, inner_header)
        event_json = json.dumps(event_data.to_dict())
        await conn.send(event_json)

    async def event_stream(self) -> AsyncGenerator[EventData, None]:
        conn = self._conn

        while True:
            try:
                data = await conn.recv()
            except Exception:
                await self._update_connection_state(ZapClientState.ERROR)
                zap_logger.error("Error receiving data from server")
                break

            json_data: dict[str, Any] = json.loads(data)

            headers = json_data.get("headers")

            if not headers:
                headers = {}

            try:
                event_data = EventData(
                    json_data["eventName"],
                    json_data.get("payload"),
                    headers,
                )
                yield event_data
            except Exception:
                await self._update_connection_state(ZapClientState.ERROR)
                zap_logger.error("Error parsing event from server")
                break

        await self._update_connection_state(ZapClientState.OFFLINE)
        zap_logger.warning("Disconnected from server")

    async def connection_state(self) -> AsyncGenerator[ZapClientState, None]:
        while True:
            yield await self._connection_state_queue.get()

    async def close(self) -> None:
        await self._conn.close()

    async def _update_connection_state(self, state: ZapClientState):
        self._current_state = state
        await self._connection_state_queue.put(state)

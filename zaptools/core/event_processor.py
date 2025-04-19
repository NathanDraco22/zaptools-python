import traceback
from typing import Any

from .websocket_connection import WebSocketConnection
from .events import EventCaller
from .events import EventContext, EventData

from zaptools.protocols import ConnectionAdapter
from zaptools.zap_logger import zap_logger


class EventProcessor:
    _connection: WebSocketConnection
    _event_caller: EventCaller
    _adapter: ConnectionAdapter

    def __init__(
        self,
        connection: WebSocketConnection,
        event_caller: EventCaller,
    ) -> None:
        self._connection = connection
        self._event_caller = event_caller
        self._adapter = connection._connection_adapter  # type: ignore

    async def notify_connected(self):
        EVENT_NAME = "connected"

        event_data = EventData(event_name=EVENT_NAME, payload={}, headers={})
        ctx = EventContext(event_data, self._connection)

        await self._event_caller.trigger_event(ctx)

    async def notify_disconnected(self):
        EVENT_NAME = "disconnected"

        event_data = EventData(event_name=EVENT_NAME, payload={}, headers={})
        ctx = EventContext(event_data, self._connection)

        await self._event_caller.trigger_event(ctx)

    async def notify_error(self, event_name: str, error: str):
        zap_logger.error(f"An error ocurred in the event '{event_name}'")
        EVENT_NAME = "error"

        event_data = EventData(
            event_name=EVENT_NAME,
            payload=f'An error occurred in the event "{event_name}" \n {error}',
            headers={},
        )

        ctx = EventContext(event_data, self._connection)

        try:
            await self._event_caller.trigger_event(ctx)
        except BaseException as e:
            zap_logger.error("An error ocurred in the a event 'error' callback")
            zap_logger.error(str(e))

    async def receive_events(self) -> bool:
        try:
            data = await self._adapter.recv_json()
        except Exception:
            return False

        await self.intercept_data(data)
        return True

    async def intercept_data(self, data: dict[str, Any]):
        event_name = data.get("eventName")
        payload = data.get("payload")
        headers = data.get("headers")
        if type(event_name) is not str:
            raise Exception("Event name must be a string")
        if type(headers) is not dict:
            headers = {}
        event_data = EventData(event_name, payload, headers)
        ctx = EventContext(event_data, self._connection)

        try:
            await self._event_caller.trigger_event(ctx)
        except BaseException:
            await self.notify_error(
                event_name=event_data.event_name,
                error=str(traceback.format_exc()),
            )

    async def start_event_stream(self) -> None:
        await self.notify_connected()

        try:
            while True:
                isReceived = await self.receive_events()

                if not isReceived:
                    break
        except Exception as e:
            zap_logger.error(f"An error ocurred in the event stream \n {str(e)}")
            await self._connection.close()

        await self.notify_disconnected()

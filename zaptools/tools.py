import uuid
import traceback
from typing import Awaitable, Callable, Any

from .protocols import ConnectionAdapter
from .zap_logger import zap_logger


EventCallback = Callable[["EventContext"], Awaitable[None]]


class RequestInfo:
    host: str
    port: int
    base_url: str

    def __init__(
        self,
        host: str,
        port: int,
        base_url: str,
    ) -> None:
        self.host = host
        self.port = port
        self.base_url = base_url


class Event:
    def __init__(
        self,
        name: str,
        callback: EventCallback,
    ) -> None:
        self.name = name
        self.callback = callback


class EventData:
    def __init__(
        self,
        event_name: str,
        payload: Any,
        headers: dict[str, Any],
    ) -> None:
        self.event_name = event_name
        self.payload = payload
        self.headers = headers

    def to_dict(self) -> dict[str, Any]:
        return {
            "eventName": self.event_name,
            "payload": self.payload,
            "headers": self.headers,
        }


class WebSocketConnection:
    id: str

    _connection_adapter: ConnectionAdapter

    def __init__(self, id: str, connection_adapter: ConnectionAdapter) -> None:
        self._connection_adapter = connection_adapter
        self.id = id

    async def send(
        self,
        event_name: str,
        payload: dict[str, Any] = {},
        headers: dict[str, Any] | None = None,
    ) -> None:
        concatenated_headers = headers

        if not concatenated_headers:
            concatenated_headers = {}

        await self._connection_adapter.send_event(
            event_name,
            payload,
            concatenated_headers,
        )

    async def close(self) -> None:
        await self._connection_adapter.close()


class EventContext:
    def __init__(self, event_data: EventData, connection: WebSocketConnection) -> None:
        self.event_data = event_data
        self.connection = connection
        self.event_name = event_data.event_name
        self.payload = event_data.payload
        self.headers = event_data.headers


class IDController:
    _ID_HEADING = "zpt"

    def eval(self, id: str | None = None) -> str:
        if id:
            return id
        return str(f"{self._ID_HEADING}-{uuid.uuid4()}")


# ------------------------------------------------------------------------------


class EventBook:
    event_records: dict[str, Event] = {}

    def save_event(self, event: Event) -> None:
        self.event_records[event.name] = event

    def get_event(self, name: str) -> Event | None:
        return self.event_records.get(name)


class EventRegister:

    def __init__(self, event_book: EventBook = EventBook()) -> None:
        self._event_book = event_book

    def on_event(self, name: str):
        def inner(callback: EventCallback):
            event = Event(name, callback)
            self._event_book.save_event(event)

        return inner


class EventCaller:
    def __init__(self, event_book: EventBook) -> None:
        self._event_book = event_book

    async def trigger_event(self, ctx: EventContext):
        event = self._event_book.get_event(ctx.event_name)

        if not event:
            return

        await event.callback(ctx)


# ----------------------------------------------------------------------------------


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


class Connector:
    _adapter: ConnectionAdapter

    def __init__(
        self,
        register: EventRegister,
        adapter_type: type[ConnectionAdapter],
        id_controller: IDController,
        event_caller: EventCaller,
    ) -> None:
        self.register = register
        self.event_caller = event_caller
        self.adapter_type = adapter_type
        self.id_controller = id_controller

    async def plug(self, websocket: ConnectionAdapter) -> EventProcessor:
        self._adapter = self.adapter_type(websocket)
        await self._adapter.start_connection()

        current_id = self.id_controller.eval()
        ws_connection = WebSocketConnection(current_id, self._adapter)

        return EventProcessor(ws_connection, self.event_caller)

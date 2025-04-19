from typing import Awaitable, Callable, Any

from .websocket_connection import WebSocketConnection

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


class EventContext:
    def __init__(self, event_data: EventData, connection: WebSocketConnection) -> None:
        self.event_data = event_data
        self.connection = connection
        self.event_name = event_data.event_name
        self.payload = event_data.payload
        self.headers = event_data.headers


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

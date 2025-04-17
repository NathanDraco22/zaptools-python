from typing import Awaitable, Protocol, Any, Callable, AsyncIterator


class ConnectionAdapter(Protocol):
    websocket: Any

    def __init__(self, websocket: Any) -> None:
        self.websocket = websocket

    async def start_connection(self) -> None: ...

    async def recv_json(self) -> dict[str, Any]: ...

    async def json_event_stream(self) -> AsyncIterator[Any]:
        yield ...

    async def send_event(
        self,
        event_name: str,
        payload: Any,
        headers: dict[str, Any] | None = None,
    ) -> None: ...

    async def close(self) -> None: ...


class Event(Protocol):
    name: str
    callback: Callable[[Any], Awaitable[None]]


class EventBook(Protocol):
    event_records: dict[str, Event]

    def save_event(self, event: Event) -> None: ...

    def get_event(self, name: str) -> Event | None: ...


class IDController(Protocol):
    _ID_HEADING = "zpt"

    def eval(self, id: str | None = None) -> str: ...

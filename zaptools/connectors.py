from typing import Any
from .core import (
    EventRegister,
    EventCaller,
    IDController,
    WebSocketConnection,
    EventProcessor,
)
from .adapters import FastApiAdapter, SanicAdapter


class FastApiConnector:
    def __init__(
        self,
        register: EventRegister,
        websocket: Any,
        connection_id: str | None = None,
    ):
        """
        Initializes a FastApiConnector instance.

        Args:
            register (EventRegister): The event register for managing events.
            websocket (Any): The websocket connection instance.
            connection_id (str | None, optional): The unique identifier for the connection. Will be generated if not provided.
        """

        self.register = register
        self.websocket = websocket
        self._connection_id = connection_id

    async def start(self) -> None:
        fastapi_adapter = FastApiAdapter(self.websocket)
        event_caller = EventCaller(self.register._event_book)  # type: ignore
        id_controller = IDController()

        await fastapi_adapter.start_connection()

        current_id = id_controller.eval(self._connection_id)
        ws_connection = WebSocketConnection(current_id, fastapi_adapter)
        event_processor = EventProcessor(ws_connection, event_caller)

        await event_processor.start_event_stream()


class SanicConnector:
    def __init__(
        self,
        register: EventRegister,
        websocket: Any,
        connection_id: str | None = None,
    ):
        """
        Initializes a SanicConnector instance.

        Args:
            register (EventRegister): The event register for managing events.
            websocket (Any): The websocket connection instance.
            connection_id (str | None, optional): The unique identifier for the connection. Will be generated if not provided.
        """
        self.register = register
        self.websocket = websocket
        self.connection_id = connection_id

    async def start(self) -> None:
        sanic_adapter = SanicAdapter(self.websocket)
        event_caller = EventCaller(self.register._event_book)  # type: ignore
        id_controller = IDController()

        await sanic_adapter.start_connection()

        current_id = id_controller.eval(self.connection_id)
        ws_connection = WebSocketConnection(current_id, sanic_adapter)
        event_processor = EventProcessor(ws_connection, event_caller)

        await event_processor.start_event_stream()

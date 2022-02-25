from typing import Callable, Coroutine

from zaptools.customtypes.types import SocketClient, FastApiZapAdapter

class SocketEvent():
    event_name: str
    callback: Callable[ [any, SocketClient , FastApiZapAdapter ], Coroutine ]

    def __init__(self, 
    event_name:str, 
    callback: Callable[[any, SocketClient, FastApiZapAdapter], Coroutine],
    ) -> None:
        self.event_name = event_name
        self.callback = callback
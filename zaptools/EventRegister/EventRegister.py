from typing import List, Callable, Coroutine

from zaptools.models.socket_event_model import SocketEvent


class EventRegister():

    _socket_events : List[SocketEvent] = []

    def on_event(self,event:str):
        def internal(my_func):
            my_func : Callable[[], Coroutine]
            socket_event = SocketEvent(event, my_func)
            self._socket_events.append(socket_event)
        return internal
    
    def get_events(self):
        return self._socket_events
    



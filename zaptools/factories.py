from typing import Any
from .tools import Event ,EventBook, EventRegister




class EventBookFactory:

    @staticmethod
    def mix_event_book(event_book1: EventBook, event_book2: EventBook):
        mixed_events = event_book1.events|event_book2.events
        new_event_book = EventBook()
        new_event_book.events = mixed_events
        return new_event_book

class EventRegisterFactory:

    @staticmethod
    def mix_register(reg1: EventRegister, reg2: EventRegister):
        new_book = EventBookFactory.mix_event_book(
            reg1._event_book,
            reg2._event_book
        )
        return EventRegister(new_book)

class EventFactory:
    @staticmethod
    def from_dict(data: dict[str, Any]) -> Event:
        return Event(
            name= data["name"],
            payload= data["payload"]
        )
    
    @staticmethod
    def event_to_dict( event: Event ) -> dict[str, Any]:
        return vars(event)
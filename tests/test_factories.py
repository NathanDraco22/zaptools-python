from zaptools.factories import EventFactory, EventBookFactory, EventRegisterFactory
from zaptools.tools import Event, EventBook, EventRegister



def test_event_factory_to_dict():
    event = Event("winter", "snow")
    event_dict = EventFactory.event_to_dict(event)
    assert event_dict["name"] == "winter" , "Event is winter"
    assert event_dict["payload"] == "snow" , "Event is winter"

def test_event_factory_from_dict():
    event_dict = {"name" : "summer", "payload":"sunlight"}
    event = EventFactory.from_dict(event_dict)
    assert event.name == "summer", "event => summer"
    assert event.payload == "sunlight", "payload => sunlight"


EVENT_NAME_1 = "winter"
EVENT_NAME_2 = "summer"

def create_2_books() -> (EventBook,EventBook):
    book1 = EventBook()
    book2 = EventBook()
    book1.events = {EVENT_NAME_1 : lambda _ : ...}
    book2.events = {EVENT_NAME_2 : lambda _ : ...}
    return (book1, book2)

def test_mix_event_book():
    book1, book2 = create_2_books()
    mixed_book = EventBookFactory.mix_event_book(book1, book2)
    mixed_events_number = len(mixed_book.events)
    mixed_keys = list(mixed_book.events.keys())
    assert mixed_events_number == 2 , "MUST 2 Events"
    assert EVENT_NAME_1 in mixed_keys
    assert EVENT_NAME_2 in mixed_keys

def test_mix_register():
    book1, book2 = create_2_books()
    reg1 = EventRegister(book1)
    reg2 = EventRegister(book2)
    mixed_reg = EventRegisterFactory.mix_register(reg1, reg2)
    mixed_book = mixed_reg._event_book
    mixed_events_number = len(mixed_book.events)
    mixed_keys = list(mixed_book.events.keys())
    assert mixed_events_number == 2 , "MUST 2 Events"
    assert EVENT_NAME_1 in mixed_keys
    assert EVENT_NAME_2 in mixed_keys

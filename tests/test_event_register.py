from zaptools.models import EventRegister, EventBook

def test_add_event():
    EVENT_NAME = "event_test"
    event_book = EventBook()
    register = EventRegister(event_book)

    @register.on_event(EVENT_NAME)
    async def demo_event(ctx):
        return
    
    callback = event_book.events.get(EVENT_NAME)
    is_key_added = callback is not None
    is_invalid_key = event_book.events.get("WRONG") is None
    callback_name = callback.__name__

    assert len(event_book.events) == 1, "Event added"
    assert is_key_added, "Event added by name"
    assert is_invalid_key, "Invalid Key"
    assert callback_name, "demo_event"

def test_add_on_connect():
    event_book = EventBook()
    register = EventRegister(event_book)

    @register.on_connected
    async def init_connection(ctx):
        return
    
    callback = event_book.on_connected_event
    is_on_connected_added = callback is not None
    callback_name = callback.__name__

    assert is_on_connected_added, "on connected event added"
    assert callback_name == "init_connection" , "name must be init_connection"

def test_add_on_disconnected():
    event_book = EventBook()
    register = EventRegister(event_book)

    @register.on_disconnected
    async def end_connection(ctx):
        return
    
    callback = event_book.on_disconnected_event
    is_on_diconnected_added = callback is not None
    callback_name = callback.__name__

    assert is_on_diconnected_added, "event on_disconnected added"
    assert callback_name == "end_connection", "name must be end_connection"

def test_multi_event_added():
    event_book = EventBook()
    register = EventRegister(event_book)

    @register.on_event("spring")
    def sprint_callback():
        return "spring!!!"
    
    @register.on_event("summer")
    def summer_callback():
        return "summer!!!"
    
    @register.on_event("autumn")
    def autumn_callback():
        return "autumn!!!"

    @register.on_event("winter")
    def winter_callback():
        return "winter!!!"
    
    event_number = len(event_book.events)
    event_items = event_book.events.items()
    for k,v in event_items:
        assert k == v()[:-3], "Callback value"
    assert event_number == 4, "4 season events"


    



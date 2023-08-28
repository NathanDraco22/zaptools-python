from zaptools.tools import EventBook


def test_regis_event():
    event_book = EventBook()
    event_book.regis_event("winter", lambda _: ...)
    event_book.events
    assert len(event_book.events) == 1, "must => 1"

def test_del_event():
    event_book = EventBook()
    event_book.regis_event("winter", lambda _: ...)
    event_book.events
    assert len(event_book.events) == 1, "must => 1"
    event_book.del_event("winter")
    assert len(event_book.events) == 0, "must => 0"

def test_get_callable():
    event_book = EventBook()
    event_book.regis_event("winter", lambda _: ...)
    callback = event_book.get_callable("winter")
    assert callback is not None
    callback = event_book.get_callable("summer")
    assert callback is None
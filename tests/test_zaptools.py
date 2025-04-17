import json
from typing import Any
from websockets.sync.client import connect, ClientConnection

SERVER_DOMAIN = "ws://localhost:8000/"


def _init_settings(check_on_connected: bool = True) -> ClientConnection:
    ws_client = connect(SERVER_DOMAIN)
    if check_on_connected:
        ws_client.recv()
    return ws_client


def test_on_connected():
    client = _init_settings(check_on_connected=False)
    data = client.recv(2.0)
    json_dict = json.loads(data)
    assert json_dict["eventName"] == "connected"
    assert json_dict["payload"]["event"] == "LIVE"
    assert json_dict["headers"]["myHeader"] == "I'm a header"
    client.close()


def test_error_case():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "error-case",
        "payload": {},
        "headers": {},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv(2.0)
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "remote_error"

    client.close()


def test_send_header():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "header",
        "payload": {},
        "headers": {"clientHeader": "client"},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv(2.0)
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "headerTest"
    assert json_dict["payload"]["isOk"] is True
    assert json_dict["headers"]["test"] == "headerTest"

    client.close()


def test_send_event1():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "event1",
        "payload": {"hello": "from client"},
        "headers": {},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "event1_completed"
    assert json_dict["payload"]["event"] == "HELLO FROM SERVER"

    client.close()


def test_send_event1_event2():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "event1",
        "payload": {"hello": "from client"},
        "headers": {},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "event1_completed", "event1 completed"
    assert json_dict["payload"]["event"] == "HELLO FROM SERVER", "payload received"

    request_data = {
        "eventName": "event2",
        "payload": {"hello": "from client"},
        "headers": {},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "event2_completed"
    assert json_dict["payload"]["event"] == "HELLO FROM SERVER 2"

    client.close()


def test_hello_bye():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "hb",
        "payload": {"hello": "from client"},
        "headers": {},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "h"
    assert json_dict["payload"]["event"] == "h event"

    try:
        client.recv()
        assert False
    except Exception:
        assert True


def test_exit():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "exit",
        "payload": {"hello": "from client"},
        "headers": {},
    }

    json_string = json.dumps(request_data)
    client.send(json_string)

    try:
        client.recv()
        assert False
    except Exception:
        assert True


def test_empty_event():
    client = _init_settings()

    request_data: dict[str, Any] = {
        "eventName": "empty-event",
    }

    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)

    assert json_dict["eventName"] == "empty-event"
    assert json_dict["payload"] is None
    assert json_dict.get("headers") is None

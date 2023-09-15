import json
from websockets.sync.client import connect, ClientConnection

SERVER_DOMAIN = "ws://localhost:8000/"

def _init_settings(check_on_connected = True) ->  ClientConnection:
    ws_client = connect(SERVER_DOMAIN)
    if check_on_connected:
        ws_client.recv()
    return ws_client

def test_on_connected():
    client = _init_settings(check_on_connected=False)
    data = client.recv(2.0)
    json_dict = json.loads(data)
    assert json_dict["eventName"] == "connected", "event1 completed"
    assert json_dict["payload"] == "LIVE", "payload received"
    client.close()


def test_send_event1():
    client = _init_settings()
    request_data = {
        "eventName": "event1",
        "payload": {"hello":"from client"}
    }
    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)
    assert json_dict["eventName"] == "event1_completed", "event1 completed"
    assert json_dict["payload"] == "HELLO FROM SERVER", "payload received"
    client.close()

def test_send_event1_event2():
    client = _init_settings()
    request_data = {
        "eventName": "event1",
        "payload": {"hello":"from client"}
    }
    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)
    assert json_dict["eventName"] == "event1_completed", "event1 completed"
    assert json_dict["payload"] == "HELLO FROM SERVER", "payload received"

    request_data = {
        "eventName": "event2",
        "payload": {"hello":"from client"}
    }
    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)
    assert json_dict["eventName"] == "event2_completed", "event1 completed"
    assert json_dict["payload"] == "HELLO FROM SERVER 2", "payload received"
    client.close()

def test_hello_bye():
    client = _init_settings()
    request_data = {
        "eventName": "hb",
        "payload": {"hello":"from client"}
    }
    json_string = json.dumps(request_data)
    client.send(json_string)
    data = client.recv()
    json_dict = json.loads(data)
    assert json_dict["eventName"] == "h", "event1 completed"
    assert json_dict["payload"] == "h event", "payload received"
    try:
        client.recv()
        assert False
    except Exception:
        assert True
    

def test_exit():
    client = _init_settings()
    request_data = {
        "eventName": "exit",
        "payload": {"hello":"from client"}
    }
    json_string = json.dumps(request_data)
    client.send(json_string)
    try:
        client.recv()
        assert False
    except Exception:
        assert True
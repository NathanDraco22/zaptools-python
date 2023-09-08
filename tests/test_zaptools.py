import json
from websockets.sync.client import connect, ClientConnection

SERVER_DOMAIN = "ws://localhost:8000/"

def _init_settings() ->  ClientConnection:
    ws_client = connect(SERVER_DOMAIN)
    return ws_client

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
    print(json_dict)
    assert json_dict["eventName"] == "event1_completed", "event1 completed"
    assert json_dict["payload"] == "HELLO FROM SERVER", "payload received"
    client.close()
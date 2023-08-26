import json
from websockets.sync.client import connect

SERVER_DOMAIN = "ws://localhost:8000/"

def test_welcome_message():
    ws_client = connect(SERVER_DOMAIN)
    message = ws_client.recv()
    message = json.loads(message.decode())
    message = json.loads(message)
    ws_client.close()
    assert message["name"] == "wellcome", "Wellcome event from server"
    pass

def test_send_event():
    ws_client = connect(SERVER_DOMAIN)
    ws_client.recv()
    data_to_send = json.dumps({"name": "event1", "payload":"HELLO FROM CLIENT"})
    ws_client.send(data_to_send)
    message = ws_client.recv()
    message = json.loads(message.decode())
    message = json.loads(message)
    ws_client.close()
    assert message["name"] == "event1_completed", "Event1 from server"
    assert message["payload"] == "HELLO FROM SERVER"
    pass

def test_send_event2():
    ws_client = connect(SERVER_DOMAIN)
    ws_client.recv()
    data_to_send = json.dumps({"name": "event1", "payload":"HELLO FROM CLIENT"})
    ws_client.send(data_to_send)
    ws_client.recv()
    data_to_send = json.dumps({"name": "event2", "payload":"HELLO FROM CLIENT"})
    ws_client.send(data_to_send)
    message = ws_client.recv()
    message = json.loads(message.decode())
    message = json.loads(message)
    ws_client.close()
    assert message["name"] == "event2_completed", "Event1 from server"
    assert message["payload"] == "HELLO FROM SERVER 2"
    pass

def test_exit_event():
    ws_client = connect(SERVER_DOMAIN)
    ws_client.recv()
    data_to_send = json.dumps({"name": "exit", "payload":"HELLO FROM CLIENT"})
    ws_client.send(data_to_send)
    try:
        message = ws_client.recv(timeout=1)
        assert False, "Connection not closed"
    except:
        assert True, "Connection Closed"
    pass
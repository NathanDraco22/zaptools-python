from zaptools.helpers import ZaptoolHelper


zap_helper = ZaptoolHelper()

def test_process_id():
    res = zap_helper.process_id(None)
    res2 = zap_helper.process_id("123")
    assert len(res) > 4, "zpt id generated"
    assert res2 == "123", "custom id"

def test_check_is_new_connection():
    mock_input = {"name" : "init", "payload" : {}}
    mock_input2 = {"name" : "init", "payload" : {"id":"123"}}
    res = zap_helper.check_is_new_connection(mock_input)
    res2 = zap_helper.check_is_new_connection(mock_input2)
    assert res, "is new connection"
    assert not res2 , "is not new connection"

def test_process_init_connection():
    mock_input = {"name" : "init", "payload" : {}}
    mock_input2 = {"name" : "init", "payload" : {"id":"123"}}
    res = zap_helper.process_init_connection(mock_input)
    res2 = zap_helper.process_init_connection(mock_input2)
    assert res.is_new, "New connection"
    assert res.event.name == "init", "Init event created"
    assert len(res.connection_id) > 3, "zpt id generated"
    assert not res2.is_new, "it is a old connection"
    assert res2.connection_id == "123", "is old connection"
    assert res2.event.name == "init", "Init2 event created"

def test_process_end_connection():
    mock_input = {"name" : "init", "payload" : {}}
    mock_input2 = {"name" : "init", "payload" : {"id":"123"}}
    identifier1 = zap_helper.process_init_connection(mock_input)
    identifier2 = zap_helper.process_init_connection(mock_input2)
    res = zap_helper.process_end_connection(identifier1)
    res2 = zap_helper.process_end_connection(identifier2)
    assert res.is_new, "New connection"
    assert res.event.name == "end", "End event created"
    assert len(res.connection_id) > 3, "zpt id generated"
    assert not res2.is_new, "it is a old connection"
    assert res2.connection_id == "123", "is old connection"
    assert res2.event.name == "end", "End2 event created"

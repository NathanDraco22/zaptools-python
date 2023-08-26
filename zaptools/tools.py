
import uuid

def process_id(id:str|None) -> str|None:
    if id : return id
    return str(uuid.uuid4().bytes)

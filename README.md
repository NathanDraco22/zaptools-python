# ZAPTOOLS

#### A toolkit for Event-Driven websocket management

### Getting Started

Zaptools provides tools for building event-driven websocket integration. It includes pre-existing classes to seamless integration with FastApi and Sanic.

#### FastAPI
```python
from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, Context, Connector
from zaptools.adapters import FastApiAdapter

app:FastAPI = FastAPI()
register: EventRegister = EventRegister() 

@register.on_event("hello") 
async def hello_trigger(context: Context):
    conn = context.connection
    await conn.send("hello", "HELLO FROM SERVER !!!") 


connector = Connector(register, FastApiAdapter)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    event_processor = await connector.plug(websocket= ws)
    await event_processor.start_event_stream()
```

Firstly create a `FastAPI` and `EventRegister` instance. `EventRegister` has the responsability to create events.
```python
from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, Context, Connector
from zaptools.adapters import FastApiAdapter

app:FastAPI = FastAPI()
register: EventRegister = EventRegister() 
```
For Creating events use the decorator syntax.
This will creates an event named `"hello"` and it will call `hello_trigger` function when an event named `"hello"` is received.
```python
@register.on_event("hello") 
async def hello_trigger(context: Context):
    conn = context.connection
    await conn.send("hello", "HELLO FROM SERVER !!!") 
```
> Event it is a class with name("hello") and the callback(hello_trigger)

`Connector` has the responsability to connect the `EventRegister` and the `Websocket` class. It must to provide an adapter type, for `FastAPI` framework it is a pre-existing adapter.
```python
connector = Connector(register, FastApiAdapter)
```
For connecting all with the websocket class provided by FastAPI framework use the `plug` method of the `Connector` instance, it will return an instance of `EventProcessor` class.
```python
@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    event_processor = await connector.plug(websocket= ws)
    await event_processor.start_event_stream()
```
Finally, `EventProcessor` has the responsability to intercept and validate data from websocket connection, To start intercepting and invoking your events, just call the `start_event_stream` method.

> Note: The operation that returns a Courutine must be Awaited
# ZAPTOOLS

#### A toolkit for Event-Driven websocket management

### Getting Started

Zaptools provides tools for building event-driven websocket integration. It includes pre-existing classes to seamless integration with FastApi and Sanic.


#### installation
``` bash
pip install zaptools # windows
pip3 install zaptools # mac
```

#### FastAPI
```python
from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, Context
from zaptools.connectors import FastApiConnector

app:FastAPI = FastAPI()
register: EventRegister = EventRegister() 

@register.on_event("hello") 
async def hello_trigger(context: Context):
    conn = context.connection
    conn.send("hello", "HELLO FROM SERVER !!!") 


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    event_processor = await FastApiConnector.plug(register, ws)
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
    conn.send("hello", "HELLO FROM SERVER !!!") 
```
> Event it is a class with name("hello") and the callback(hello_trigger)

For connecting `EvenRegister` with the websocket class provided by FastAPI framework, there is a `FastApiConnector`, use the `plug` static method of the `FastApiConnector`, it will return an instance of `EventProcessor` class.
```python
@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    event_processor = await connector.plug(websocket= ws)
    await event_processor.start_event_stream()
```
Finally, `EventProcessor` has the responsability to intercept and validate data from websocket connection. To start intercepting and invoking your events, just call the `start_event_stream` method.

It's the same way for Sanic Framework
#### Sanic
```python
from sanic import Sanic, Request, Websocket

from zaptools.tools import EventRegister, Context
from zaptools.connectors import SanicConnector

app = Sanic("MyHelloWorldApp")
register: EventRegister = EventRegister()

@register.on_event("hello") 
async def hello_trigger(context: Context):
    conn = context.connection
    conn.send("hello", "HELLO FROM SERVER !!!") 

@app.websocket("/")
async def websocker(request: Request, ws: Websocket):
    event_processor = await SanicConnector.plug(register ,ws)
    await event_processor.start_event_stream()
```
### Context object
Each element is triggered with a `Context` object. This `Context` object contains information about the current event and which `WebSocketConnection` is invoking it.
```python
Context.event_name # name of current event
Context.payload # payload the data from the connection
Context.connection # WebSocketConnection 
```
### Sending Events
In order to response to the client use the `WebSocketConnection.send(event:str, payload:Any)`, this object is provided by the `Context`.
```python
@register.on_event("hello") 
async def hello_trigger(context: Context):
    conn = context.connection
    conn.send("hello", "HELLO FROM SERVER !!!") # sending "hello" event to client with a payload.
```
### WebSocketConnection
`WebSocketConnection` provides a easy interaction with the websocket.

```python
WebSocketConnection.id # ID of connection

WebSocketConnection.send(event:str, payload:Any) #Send Event to the client

WebSocketConnection.close() # Close the websocket connection
```

### Events

The `"connected"` and `"disconnected"` events can be used to trigger an action when a connection is started and after it is closed.

```python
@register.on_event("connected")
async def connected_trigger(context: Context):
    print("Connection started")

@register.on_event("disconnected")
async def disconnected_trigger(context:Context):
    print("Connection closed")
```

### What's next
- [X] support for events
- [ ] share message between multiple WebSockets

## Contributions are wellcome

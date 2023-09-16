from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, Context
from zaptools.connectors import FastApiConnector

app:FastAPI = FastAPI()
register: EventRegister = EventRegister()

@register.on_event("connected")
async def connected_trigger(ctx: Context):
    ctx.connection.send("connected", "LIVE", {"myHeader": "I'm a header"})

@register.on_event("disconnected")
async def disconnected_trigger(ctx:Context):
    print(f"connection left -> {ctx.connection.id}")

@register.on_event("header")
async def headers( ctx:Context):
    test_header = ctx.headers["clientHeader"]
    ctx.connection.send("headerTest", "headerTest", {"isOk" : test_header=="client"})

@register.on_event("event1")
async def event1_triger(ctx: Context):
    ctx.connection.send("event1_completed", "HELLO FROM SERVER")

@register.on_event("event2")
async def event2_triger(ctx: Context):
    ctx.connection.send("event2_completed", "HELLO FROM SERVER 2")

@register.on_event("exit")
async def exit_event( ctx: Context ):
    ctx.connection.close()

@register.on_event("hb")
async def hello_and_bye(ctx:Context):
    conn = ctx.connection
    conn.send("h", "h event")
    conn.close()

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await FastApiConnector.plug_and_start(register,ws)
from fastapi import FastAPI, WebSocket
from zaptools.tools import EventRegister, Context, Connector
from zaptools.adapters import FastApiAdapter

app:FastAPI = FastAPI()
register: EventRegister = EventRegister()

@register.on_event("connected")
async def connected_trigger(context: Context):
    await context.connection.send("connected", "LIVE")

@register.on_event("disconnected")
async def disconnected_trigger(context:Context):
    print("Connection closed")

@register.on_event("event1")
async def event1_triger(ctx: Context):
    await ctx.connection.send("event1_completed", "HELLO FROM SERVER")

@register.on_event("event2")
async def event2_triger(ctx: Context):
    await ctx.connection.send("event2_completed", "HELLO FROM SERVER 2")

@register.on_event("exit")
async def exit_event( ctx: Context ):
    await ctx.connection.close()


connector = Connector(register, FastApiAdapter)

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    event_processor = await connector.plug(websocket= ws)
    await event_processor.start_event_stream()

        
zaptools
========

PreAlfa 2

ZapTools is wrapper to handle websocket connection, based on events to a nice and smooth integration.

Usage
-----

How to use **zaptools**
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from fastapi import FastAPI
    from zaptools import FastApiZapAdapter, SocketClient

    app : FastAPI = FastAPI()
    adapter = FastApiZapAdapter(app= app, route= "/" )

    @adapter.on_client_connected
    async def on_connected(client : SocketClient , adapter : FastApiZapAdapter):
        print("client connected : ", client.id_connection)
        await client.send_event("myEvent", "Data Payload to send")

    @adapter.on_event("event")
    async def event(payload, client:SocketClient , adapter : FastApiZapAdapter ):
        print(payload)
        await client.send_event("anyEvent", {"msg" : "a Json Format"})

    @adapter.on_client_disconnected
    async def client_disconected(client : SocketClient , adapter : FastApiZapAdapter):
        print("client disconnected: ", client.id_connection)


**zaptools** is only compatible with FastAPI apps, so we need to create 
a **FastAPI** app and then create a instance of *FastApiZapAdapter*, the constructor
need the app (FastApi app) and a specific route ("/")

.. code-block:: python

    app : FastAPI = FastAPI()
    adapter = FastApiZapAdapter(app= app, route= "/" )

Now we can use the :code:`adapter` to define the function to be called
when a event is triggered, for example is we need to check if a new client
is connected to our Socket server, and then response to client:

.. code-block:: python

    @adapter.on_client_connected
    async def on_connected(client : SocketClient , adapter : FastApiZapAdapter):
        print("client connected : ", client.id_connection)
        await client.send_event("myEvent", "Data Payload to send")

the :code:`SocketClient` is a class that have :code:`id_connection` and :code:`send_event` method,
remember ever :code:`await` the :code:`send_event`.

Also, you can define a function to be called when a client is disconnected:

.. code-block:: python

    @adapter.on_client_disconnected
    async def client_disconected(client : SocketClient , adapter : FastApiZapAdapter):
        print("client disconnected: ", client.id_connection)

We can register a event, in this case we have the payload:

.. code-block:: python

    @adapter.on_event("eventName")
    async def event(payload, client:SocketClient , adapter : FastApiZapAdapter ):
        print(payload)
        await client.send_event("eventName", {"msg" : "a Json Format"})

And finally, start the FastAPI app normally (uvicorn)


Installation
------------

:code:`pip install zaptools`


Requirements
------------

FastApi



Compatibility
-------------

Python 3.7+

Licence
-------

MIT

Authors
-------
zaptools was written by Nathan Mejia
import asyncio

from random import random

import websockets
import time

async def hello():
    async with websockets.connect('ws://localhost:2028') as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))
        for i in range(0,1000):
            if random() < 0.5:
                await websocket.send('1C')
            else:
                await websocket.send('1E')

asyncio.get_event_loop().run_until_complete(hello())

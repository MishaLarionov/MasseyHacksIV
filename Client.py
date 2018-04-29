import asyncio
import websockets
import time

async def hello():
    async with websockets.connect('ws://10.88.196.214:2018') as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))
        while True:
            time.sleep(1)
            await websocket.send('testing 123 from ' + name)

asyncio.get_event_loop().run_until_complete(hello())

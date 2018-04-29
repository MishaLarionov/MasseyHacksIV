# Webserver to take the distance between ultrasonic sensor and feet
# Sensors should have to connect to the websocket? idk

import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print("< {}".format(name))

    greeting = "Hello {}!".format(name)
    await websocket.send(greeting)
    print("> {}".format(greeting))

start_server = websockets.serve(hello, 'localhost', 2018)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

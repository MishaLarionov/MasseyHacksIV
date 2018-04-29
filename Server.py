# Webserver to take the distance between ultrasonic sensor and feet
# Sensors should have to connect to the websocket? idk

import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    global connected

    connected.add(websocket)
    try:
        await asyncio.wait([ws.send("register") for ws in connected])
    finally:
        while True:
            print(await websocket.recv())

start_server = websockets.serve(handler, 'localhost', 2018)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

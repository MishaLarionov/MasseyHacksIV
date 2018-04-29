# Webserver to take the distance between ultrasonic sensor and feet
# Sensors should have to connect to the websocket? idk

import asyncio
import websockets

from keypresshandler import PressKey, ReleaseKey

# Define the keys
KEY_W = 0x57
KEY_A = 0x41
KEY_S = 0x53
KEY_D = 0x44

connected = set()
lastDir = ["1E", "2E"]

# Socket handler
async def handler(websocket, path):
    global connected
    global lastDir
    connected.add(websocket)
    try:
        await asyncio.wait([ws.send("register") for ws in connected])
    finally:
        while True:
            dir_input = await websocket.recv()
            # Decide whether we got a new input
            #   1C
            # 1F  2F
            #   2C
            print(dir_input)
            if dir_input.startswith("1") and dir_input != lastDir[0]:
                # 1C = front
                # 1F = left
                ReleaseKey(KEY_W)
                ReleaseKey(KEY_A)
                if dir_input == "1C":
                    PressKey(KEY_W)
                elif dir_input == "1F":
                    PressKey(KEY_A)

                lastDir[0] = dir_input

            elif dir_input.startswith("2") and dir_input != lastDir[1]:
                # 2C = back
                # 2F = right

                lastDir[1] = dir_input

start_server = websockets.serve(handler, None, 2028)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

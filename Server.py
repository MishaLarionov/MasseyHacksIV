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

#   1
# 4   2
#   5

# 0 = 1 NOR 2
# 3 = 4 NOR 5
connected = set()
lastDir = ["0", "3"]

# Socket handler
async def handler(websocket, path):
    global connected
    global lastDir
    connected.add(websocket)
    print("new client connected")
    # try:
    #     await asyncio.wait([ws.send("register") for ws in connected])
    # finally:
    while True:
        dir_input = await websocket.recv()
        # Decide whether we got a new input
        #   1C
        # 1F  2F
        #   2C
        print(dir_input)
        if int(dir_input) < 3 and dir_input != lastDir[0]:
            # 1 = front
            # 2 = right
            ReleaseKey(KEY_W)
            ReleaseKey(KEY_D)
            if dir_input == "1":
                PressKey(KEY_W)
            elif dir_input == "2":
                PressKey(KEY_D)

            lastDir[0] = dir_input

        elif int(dir_input) >= 3 and dir_input != lastDir[1]:
            # 5 = back
            # 4 = left
            ReleaseKey(KEY_S)
            ReleaseKey(KEY_A)
            if dir_input == "5":
                PressKey(KEY_S)
            elif dir_input == "4":
                PressKey(KEY_A)

            lastDir[1] = dir_input

start_server = websockets.serve(handler, None, 2028)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

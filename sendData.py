import asyncio
import websockets
import json
import random
import basictests

async def hello(websocket: websockets.WebSocketServer):
    while True:
        name = await websocket.recv()
        print(f"<<< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f">>> {greeting}")


async def clientHandler(websocket: websockets.WebSocketServer):

    try:
        while True:
            recievedJSON = await websocket.recv()
            requestjson = json.loads(recievedJSON)

            match requestjson['code']:
                case "get3":
                    output = dict()
                    output['code'] = 'get3Response'
                    output['response'] = basictests.generateRandomAverage(2)
                    random.shuffle(output['response'])
                    jsonOutput = json.dumps(output)
                    await websocket.send(jsonOutput)
                case _:
                    print("Recieved unknown code")

    except websockets.exceptions.ConnectionClosedOK:
        print("Client closed connection abruptly (OK)")



async def main():
    async with websockets.serve(clientHandler, "localhost", 5050):
        await asyncio.Future()  # run forever





if __name__ == "__main__":
    asyncio.run(main())

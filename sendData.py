import asyncio
import websockets
import json
import random
import basictests

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

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
            output = dict()

            # requestjson follow the following syntax:
            # 'code' is always all lowercase. responses from server have the 'response' suffix
            # first code, then response, then else
            match requestjson['code']:
                case "get3":
                    output['code'] = 'get3response'
                    output['response'] = basictests.generateRandomAverage(2)
                    print(output['response'])
                    random.shuffle(output['response'])

                case "check3":
                    output['code'] = 'check3response'
                    requestjson['solution'][1], requestjson['solution'][2] = requestjson['solution'][2], requestjson['solution'][1] #swap elems to fit function checkAverage
                    output['response'] = basictests.checkAverage(requestjson['solution'])

                case _:
                    print("Recieved unknown code")

            jsonOutput = json.dumps(output)
            await websocket.send(jsonOutput)


    except websockets.exceptions.ConnectionClosedOK:
        print("Client closed connection abruptly (OK)")



async def main():
    async with websockets.serve(clientHandler, "3.91.255.112", 5050):
        await asyncio.Future()  # run forever





if __name__ == "__main__":
    asyncio.run(main())

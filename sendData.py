import asyncio
import websockets
import json
import random
import basictests
import clientid
from datetime import timedelta

# hardcoding how long each task should be open for here:
get3Time = timedelta(seconds=60)

def terminationOutput():
    '''Generates termination output json. This is what is sent to client when they ask for a response,
    but should not get one (ie, after time runs out).'''
    output = dict()
    output['code'] = "terminate"

    return output


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

            # requestjson has the following syntax:
            # requestjson['code'] is always all lowercase and numeric. responses from server have the 'response' suffix

            match requestjson['code']:
                case "getid":
                    task = requestjson['task']
                    output['code'] = 'getidresponse'
                    output['response'] = newID = clientid.getNewID()
                    clientid.setIDtask(newID, task)


                case "get3":
                    try:
                        newID = requestjson['id']
                        if (clientid.isIDInTask(newID, get3Time, "get3")):
                            output['code'] = 'get3response'
                            output['response'] = basictests.generateRandomAverage(2)
                            print(output['response'])
                            random.shuffle(output['response'])
                        else:
                            output = terminationOutput()
                    except KeyError:
                        print("Recieved malformed json", requestjson['code'])


                case "check3":
                    try:
                        newID = requestjson['id']
                        if (clientid.isIDInTask(newID, get3Time, "get3")):
                            output['code'] = 'check3response'
                            requestjson['solution'][1], requestjson['solution'][2] = requestjson['solution'][2], requestjson['solution'][1] #swap elems to fit function checkAverage
                            output['response'] = basictests.checkAverage(requestjson['solution'])
                        else:
                            output = terminationOutput()
                    except KeyError:
                        print("Recieved malformed json", requestjson['code'])



                case _:
                    print("Recieved unknown code")

            jsonOutput = json.dumps(output)
            await websocket.send(jsonOutput)


    except websockets.exceptions.ConnectionClosedOK:
        print("Client closed connection abruptly (OK)")
    except websockets.exceptions.ConnectionClosed:
        print("Client closed connection abruptly (No Closing Message)")



async def main():
    async with websockets.serve(clientHandler, "", 5050):
        await asyncio.Future()  # run forever





if __name__ == "__main__":
    asyncio.run(main())

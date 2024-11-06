import asyncio
import websockets
import json
import random
import basictests
import clientid
import os
import signal

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
                # below are id related codes
                case "getid":
                    task = requestjson['task']
                    output['code'] = 'getidresponse'
                    output['response'] = newID = clientid.getNewID()
                    clientid.setIDtask(newID, task)

                case "checkid":
                    try:
                        newID = requestjson['id']
                        task = requestjson['task']
                        output['code'] = 'checkidresponse'
                        output['response'] = not clientid.isIDInTask(newID, task)
                    except KeyError:
                        print("Recieved malformed json", requestjson['code'])

                # below are 'get3' related codes
                case "get3":
                    try:
                        newID = requestjson['id']
                        if (clientid.isIDInTask(newID, "get3")):
                            output['code'] = 'get3response'
                            output['response'] = basictests.generateSimDiff(2)
                            print(output['response'])
                            random.shuffle(output['response']) # maybe this isnt secure enough? its probably ok for now
                        else:
                            output = terminationOutput()
                    except KeyError:
                        print("Recieved malformed json", requestjson['code'])


                case "check3":
                    try:
                        newID = requestjson['id']
                        if (clientid.isIDInTask(newID, "get3") and clientid.checkLastInteraction(newID, 1)):
                            output['code'] = 'check3response'
                            # requestjson['solution'][1], requestjson['solution'][2] = requestjson['solution'][2], requestjson['solution'][1] #swap elems to fit function checkAverage
                            response = basictests.checkSimDiff(requestjson['solution'])

                            if (not response):
                                clientid.markIDTime(newID)

                            output['response'] = response
                        else:
                            output = terminationOutput()
                    except KeyError:
                        print("Recieved malformed json", requestjson['code'])



                # base case
                case _:
                    print("Recieved unknown code")

            jsonOutput = json.dumps(output)
            await websocket.send(jsonOutput)


    except websockets.exceptions.ConnectionClosedOK:
        print("Client closed connection abruptly (OK)")
    except websockets.exceptions.ConnectionClosed:
        print("Client closed connection abruptly (No Closing Message)")



async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "5150"))

    async with websockets.serve(clientHandler, "", port):
        await stop





if __name__ == "__main__":
    asyncio.run(main())

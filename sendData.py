import asyncio
import websockets
import basictests

async def hello(websocket: websockets.WebSocketServer):
    while True:
        name = await websocket.recv()
        print(f"<<< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f">>> {greeting}")

async def main():
    async with websockets.serve(hello, "localhost", 5050):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

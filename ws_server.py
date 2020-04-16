import asyncio
from typing import Set, Callable

import websockets
from websockets.http import Headers
from websockets.server import Serve

clients: Set = set()


class WebSocketServer:
    _on_client_connected: Callable = None

    def __init__(self, port: int, host: str):
        self.port = port
        self.host = host

    async def connect(self):
        loop = asyncio.get_event_loop()
        server: Serve = websockets.serve(
            self.wait_for_clients,
            "localhost",
            8765,
            process_request=self.process_request
        )

        loop.run_until_complete(server)
        print("server started", server)
        loop.run_forever()

    async def wait_for_clients(self, ws: websockets.WebSocketServerProtocol, path: str):
        print("started")

        if ws not in clients:
            # Authenticate
            print("New! + registering client...")
            clients.add(ws)
            self._on_client_connected(ws)
            await self.listen_to_client(ws)
            print("test")
            # start_new_thread(listen_to_client, (ws,))
            header = ws.request_headers.get('Authorization')
            # if header == 'Basic cm9vdDo3NzA3NzA=':
            #     print("Authenticated. + registering client...")
            #     clients.add(ws)
            # else:
            #     print("- unregistering client...")
            #     clients.remove(ws)
        else:
            pass
            # print("listening to client...")
            #
            # name = await ws.recv()
            # print(f"client:  {name}")
            #
            # greeting = f"Echo {name}!"
            #
            # await ws.send(greeting)
            # print(f"server:  {greeting}")
        print("ended")

    # Blocking
    async def listen_to_client(self, ws: websockets.WebSocketServerProtocol):
        # print("listening to client...")
        while True:
            message = await ws.recv()
            self.on_message(ws, message)

    def on_message(self, ws: websockets.WebSocketServerProtocol, msg: str):
        print(f"Received new message [{msg}]")
        self.broadcast(msg)

    # Cant use this as async definition
    async def broadcast(self, message: str):
        for ws in clients:
            print(f"Sending [{message}] to ", ws)
            await ws.send(message)

    # Runs before ws_handler
    def process_request(self, path: str, headers: Headers):
        auth = headers.get("Authorization")
        print(f"process_request with path {path}, and token: {auth}")

    def set_fn_new_client(self, on_new_client: Callable):
        self._on_client_connected = on_new_client


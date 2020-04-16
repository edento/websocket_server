import asyncio
from typing import Set, Callable

import websockets
from websockets.http import Headers
from websockets.server import Serve, WebSocketServerProtocol

clients: Set = set()


class WebSocketServer:
    # Callbacks for outside usage
    _on_new_message: Callable = None

    def __init__(
            self,
            port: int,
            host: str,

            on_new_message: Callable):
        self.port = port
        self.host = host
        self._on_new_message = on_new_message

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

    async def wait_for_clients(self, ws: WebSocketServerProtocol, path: str):
        print("Started waiting for clients")
        if ws not in clients:
            authorized: bool = self.auth_user(ws)
            await self.listen_to_client(ws)
            if authorized:
                print("New authorized user!")
                clients.add(ws)
                self._on_client_connected(ws)
            else:
                # print("New unauthorized client, disconnecting...")
                clients.remove(ws)

    def auth_user(self, ws: WebSocketServerProtocol) -> bool:
        header = ws.request_headers.get('Authorization')
        # Do some check here, return False if user is not authorized
        return True

    # Blocking
    async def listen_to_client(self, ws: WebSocketServerProtocol):
        # print("listening to client...")
        while True:
            message = await ws.recv()
            self.on_message(ws, message)

    def on_incoming_message(self, ws: WebSocketServerProtocol, msg: str):
        print(f"Received new message [{msg}]")
        # invoke external callback
        self._on_new_message(msg)

    # Cant use this as async definition
    async def broadcast(self, message: str):
        for ws in clients:
            print(f"Sending [{message}] to ", ws)
            await ws.send(message)

    # Runs before ws_handler
    def process_request(self, path: str, headers: Headers):
        auth = headers.get("Authorization")
        print(f"process_request with path {path}, and token: {auth}")



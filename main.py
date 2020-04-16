import asyncio
from _thread import start_new_thread
import time

from flask import Flask
from ws_server import WebSocketServer

app = Flask(__name__)

_TAG = '[Main]'
ws_server: WebSocketServer = None

# TypeError: The view function did not return a valid response.
# The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a coroutine.
@app.route('/broadcast', methods=['GET'])
async def flask_broadcast():
    message = "some dummy msg"
    # How can I use this without making flask_broadcast a coroutine?
    await ws_server.broadcast(message)
    return {"res": "eden"}

# Blocking
def start_http_server(port: int) -> None:
    print(f'{_TAG} starting with port {port}')
    app.run("0.0.0.0", 5000, debug=False, threaded=True)

# Without 'async': SyntaxError: 'await' outside async function
async def init_web_socket_as_server(port: int, host: str) -> None:
    global ws_server
    ws_server = WebSocketServer(port, host, on_new_message)
    # Without 'await': RuntimeWarning: coroutine 'WebSocketServer.connect' was never awaited
    await ws_server.connect()

async def on_new_message(message: str) -> None:
    # For example, whenever there's a new message, ask the ws_server to broadcast it
    # await ws_server.broadcast(message)
    # Do some outside logic
    pass

def broadcast_sync(message):
    time.sleep(2)

async def broadcast_async(message):
    asyncio.sleep(2)

def init() -> None:
    ws_port = 8765
    rest_port = 5000
    start_new_thread(start_http_server, (rest_port,))
    # await init_web_socket_as_server(ws_port, "localhost")

if __name__ == '__main__':
    # Error: SyntaxError: 'await' outside function
    init()

    # Just runs the server forever
    while True:
        pass

from _thread import start_new_thread
from flask import Flask

from ws_server import WebSocketServer

app = Flask(__name__)

app_prefix = '/api'
_TAG = '[Main]'
ws_server: WebSocketServer = None

@app.route('/broadcast', methods=['GET'])
def broadcast():
    return {"res": "eden"}

# Blocking
def start_http_server(port: int) -> None:
    print(f'{_TAG} starting with port {port}')
    app.run("0.0.0.0", 5000, debug=False, threaded=True)

# Without 'async': SyntaxError: 'await' outside async function
async def init_web_socket_as_server(port: int, host: str) -> None:
    global ws_server
    ws_server = WebSocketServer(port, host)
    # Without 'await': RuntimeWarning: coroutine 'WebSocketServer.connect' was never awaited
    await ws_server.connect()

async def init() -> None:
    ws_port = 8765
    rest_port = 5000
    start_new_thread(start_http_server, (rest_port,))
    await init_web_socket_as_server(ws_port, "localhost")

if __name__ == '__main__':
    # Error: SyntaxError: 'await' outside function
    init()

    # Just runs the server forever
    while True:
        pass

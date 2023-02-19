import websockets
import asyncio
from utils.logger import Logger
from proto.lib.rafi12.ready2scanlate import SocketMessage

WS_LOG = Logger("WS")
SESSIONS = {}

async def main(port):
    async with websockets.serve(on_message, "0.0.0.0", port):
        WS_LOG.log(f"Websocket server started in port {port}")
        await asyncio.Future()

def start(port=5005):
    asyncio.run(main(port))

async def on_message(socket):
    WS_LOG.log(f"{socket.remote_address[0]}:{socket.remote_address[1]} connected!")
    SESSIONS.update({ f"{socket.remote_address[0]}:{socket.remote_address[1]}": socket })
    async for message in socket:
        await handle_message(message, socket)
    WS_LOG.log(f"{socket.remote_address[0]}:{socket.remote_address[1]} disconnected!")
    SESSIONS.pop(f"{socket.remote_address[0]}:{socket.remote_address[1]}")

async def handle_message(raw_msg, socket):
    try:
        msg = SocketMessage().parse(raw_msg)
        print(msg)
    except:
        WS_LOG.log(f"{socket.remote_address[0]}:{socket.remote_address[1]} sent an invalid message!")
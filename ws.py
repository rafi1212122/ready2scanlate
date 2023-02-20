import websockets
import asyncio
import importlib
from utils.logger import Logger
from proto.lib.rafi12.ready2scanlate import SocketMessage
from betterproto import Casing
from utils.json_writer import JsonOcr

JSON_OCR = JsonOcr('models/manga-ocr-base', 'models/comictextdetector.pt')
WS_LOG = Logger("WS")
SESSIONS = {}
JOBS_RESULT = {}

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
    msg = SocketMessage().parse(raw_msg).to_dict(casing=Casing.SNAKE)
    WS_LOG.log(f"{''.join(word.title() for word in list(msg.keys())[0].split('_'))} received!")
    await importlib.import_module(f"packet_handlers.{list(msg.keys())[0]}").handler(msg[list(msg.keys())[0]], socket)
    # try:
    #     try:
    #     except Exception as e:
    #         WS_LOG.log(f"{list(msg.keys())[0]} unhandled!: {e}")
    # except:
    #     WS_LOG.log(f"{socket.remote_address[0]}:{socket.remote_address[1]} sent an invalid message!")
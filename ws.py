import websockets
import asyncio
import importlib
import socketserver
from utils.logger import Logger
from proto.lib.rafi12.ready2scanlate import SocketMessage
from betterproto import Casing
from http import server
from threading import Thread
from core import R2S

JSON_OCR = R2S()
WS_LOG = Logger("WS")
HTTP_LOG = Logger("HTTP")
SESSIONS = {}
JOBS_RESULT = {}

def start_demo():
    class HTTPHandler(server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.path = "/dist"+self.path
            return server.SimpleHTTPRequestHandler.do_GET(self)
    http_server = socketserver.TCPServer(("0.0.0.0", 5000), HTTPHandler)
    HTTP_LOG.log("HTTP ws demo server started in port 5000!")
    http_server.serve_forever()

async def main(port):
    async with websockets.serve(on_message, "0.0.0.0", port):
        demo_thread = Thread(target=start_demo)
        demo_thread.start()
        WS_LOG.log(f"Websocket server started in port {port}!")
        await asyncio.Future()
        
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
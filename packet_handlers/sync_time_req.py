import time
import proto.lib.rafi12.ready2scanlate as ready2scanlate
from ws import WS_LOG

async def handler(packet: ready2scanlate.SyncTimeReq, socket):
    rsp = { "sync_time_rsp": { "server_time": int(time.time()), "client_time": packet["client_time"] } }
    msg = ready2scanlate.SocketMessage().from_dict(rsp).SerializeToString()
    await socket.send(msg)
    WS_LOG.log(f"{''.join(word.title() for word in list(rsp.keys())[0].split('_'))} sent!")
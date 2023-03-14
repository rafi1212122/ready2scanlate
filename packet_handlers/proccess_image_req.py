import uuid
import proto.lib.rafi12.ready2scanlate as ready2scanlate
from numpy import asarray
from PIL import Image
from io import BytesIO
from ws import WS_LOG, JSON_OCR, JOBS_RESULT
from base64 import b64decode

async def handler(packet: ready2scanlate.ProccessImageReq, socket):
    job_id = str(uuid.uuid4())
    rsp = { "proccess_image_rsp": { "job_id": job_id, "retcode": ready2scanlate.ProccessImageRspRetcode.SUCC } }
    msg = ready2scanlate.SocketMessage().from_dict(rsp).SerializeToString()
    await socket.send(msg)
    WS_LOG.log(f"{''.join(word.title() for word in list(rsp.keys())[0].split('_'))} sent!")
    open("results/tmp/wtest.png", 'wb').write(b64decode(packet["image"]))
    JOBS_RESULT.update({ job_id: JSON_OCR(asarray(Image.open(BytesIO(b64decode(packet["image"]))))) })
    notify_rsp = { "notify_job_done": { "job_id": job_id } }
    await socket.send(ready2scanlate.SocketMessage().from_dict(notify_rsp).SerializeToString())
    WS_LOG.log(f"{''.join(word.title() for word in list(notify_rsp.keys())[0].split('_'))} sent!")
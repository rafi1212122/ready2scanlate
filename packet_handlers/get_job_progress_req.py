import proto.lib.rafi12.ready2scanlate as ready2scanlate
from ws import WS_LOG, JOBS_RESULT

async def handler(packet: ready2scanlate.GetJobProgressReq, socket):
    try:
        job_status = JOBS_RESULT.get(packet["job_id"])
        rsp = { "get_job_progress_rsp": { "job": { "job_id": packet["job_id"], "progress": ready2scanlate.JobProgress.JOB_DONE if job_status else ready2scanlate.JobProgress.JOB_ON_PROGRESS, "json_out": str(job_status) if job_status else "" } } }
        msg = ready2scanlate.SocketMessage().from_dict(rsp).SerializeToString()
        await socket.send(msg)
        WS_LOG.log(f"{''.join(word.title() for word in list(rsp.keys())[0].split('_'))} sent!")
    except Exception as e:
        rsp = { "get_job_progress_rsp": { "job": { "job_id": packet["job_id"], "progress": ready2scanlate.JobProgress.JOB_DONE if job_status else ready2scanlate.JobProgress.JOB_FAILED } } }
        WS_LOG.log(f"packet: {packet}, exception: {e}")
        msg = ready2scanlate.SocketMessage().from_dict(rsp).SerializeToString()
        await socket.send(msg)
        WS_LOG.log(f"{''.join(word.title() for word in list(rsp.keys())[0].split('_'))} sent!")
        
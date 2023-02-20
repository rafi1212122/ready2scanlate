# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: ready2scanlate.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


class ProccessImageRspRetcode(betterproto.Enum):
    SUCC = 0
    FAIL = 1


class JobProgress(betterproto.Enum):
    JOB_DONE = 0
    JOB_FAILED = 1
    JOB_ON_PROGRESS = 2


@dataclass
class SyncTimeReq(betterproto.Message):
    client_time: int = betterproto.int32_field(1)


@dataclass
class SyncTimeRsp(betterproto.Message):
    server_time: int = betterproto.int32_field(1)
    client_time: int = betterproto.int32_field(2)


@dataclass
class ProccessImageReq(betterproto.Message):
    image: bytes = betterproto.bytes_field(1)


@dataclass
class ProccessImageRsp(betterproto.Message):
    retcode: "ProccessImageRspRetcode" = betterproto.enum_field(1)
    job_id: str = betterproto.string_field(2)


@dataclass
class GetJobProgressReq(betterproto.Message):
    job_id: str = betterproto.string_field(1)


@dataclass
class GetJobProgressRsp(betterproto.Message):
    job: "Job" = betterproto.message_field(1)


@dataclass
class NotifyJobDone(betterproto.Message):
    job_id: str = betterproto.string_field(1)


@dataclass
class SocketMessage(betterproto.Message):
    sync_time_req: "SyncTimeReq" = betterproto.message_field(1, group="message")
    sync_time_rsp: "SyncTimeRsp" = betterproto.message_field(2, group="message")
    proccess_image_req: "ProccessImageReq" = betterproto.message_field(
        3, group="message"
    )
    proccess_image_rsp: "ProccessImageRsp" = betterproto.message_field(
        4, group="message"
    )
    get_job_progress_req: "GetJobProgressReq" = betterproto.message_field(
        5, group="message"
    )
    get_job_progress_rsp: "GetJobProgressRsp" = betterproto.message_field(
        6, group="message"
    )
    notify_job_done: "NotifyJobDone" = betterproto.message_field(7, group="message")


@dataclass
class Job(betterproto.Message):
    job_id: str = betterproto.string_field(1)
    progress: "JobProgress" = betterproto.enum_field(2)
    json_out: str = betterproto.string_field(3, group="opt_json")

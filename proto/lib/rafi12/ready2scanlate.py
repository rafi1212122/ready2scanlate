# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: ready2scanlate.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass
class SyncTimeReq(betterproto.Message):
    client_time: int = betterproto.int32_field(1)


@dataclass
class SyncTimeRsp(betterproto.Message):
    server_time: int = betterproto.int32_field(1)


@dataclass
class SocketMessage(betterproto.Message):
    sync_time_req: "SyncTimeReq" = betterproto.message_field(1, group="message")
    sync_time_rsp: "SyncTimeRsp" = betterproto.message_field(2, group="message")

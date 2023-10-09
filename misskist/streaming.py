from __future__ import annotations
from .enums import ChannelType
from .note import Note

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class StreamingClient:
    def __init__(self, client: Client, socket):
        self.client = client
        self.socket = socket

    @classmethod
    async def connect(cls, client: Client):
        socket = await client._rest.ws_connect()
        self = cls(client, socket)
        return self

    async def get_event_always(self):
        while not self.socket.closed:
            await self.poll_event()

    async def poll_event(self):
        data = await self.socket.receive_json()
        if data["type"] == "channel":
            id_ = data["body"]["id"]
            if data["body"]["type"] == "note":
                self.client.channels[id_].dispatch(
                    "on_note", Note(data["body"]["body"])
                )

    async def connect_channel(self, channel: ChannelType):
        id_ = str(uuid.uuid4())
        data = {
            "type": "connect",
            "body": {
                "id": id_,
            },
        }
        if channel == ChannelType.global_timeline:
            data["body"]["channel"] = "globalTimeline"
            await self.send_json(data)
        return id_

    async def send_json(self, data: dict):
        await self.socket.send_json(data)

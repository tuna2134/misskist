from __future__ import annotations
from .http import RestAPI
from .streaming import StreamingClient
from .enums import ChannelType, NoteVisibility
from .note import Note

from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .events import Channel

from asyncio import AbstractEventLoop


class Client:
    def __init__(
        self,
        endpoint: str,
        *,
        ssl: bool = True,
        loop: Optional[AbstractEventLoop] = None,
    ):
        self._rest = RestAPI(endpoint, loop=loop, ssl=ssl)
        self._streaming = None
        self._not_connected = True
        self.loop = loop
        self.channels = {}
        self._wait_channels = []

    async def on_connect(self):
        self._not_connected = False
        for channel in self._wait_channels:
            await channel._connect()
            self.channels[channel.uid] = channel

    def set_token(self, token: str):
        self._rest.token = token

    async def connect(self, token: str):
        self._streaming = await StreamingClient.connect(self, token)
        self.loop.create_task(self.on_connect())
        await self._streaming.get_event_always()

    async def start(self, token: str):
        self.set_token(token)
        await self.connect(token)

    async def add_channel(self, channel: Channel):
        channel._inject(self)
        if not self._not_connected:
            await channel._connect()
            self.channels[channel.uid] = channel
        else:
            self._wait_channels.append(channel)

    async def create_note(
        self,
        text: Optional[str] = None,
        *,
        visibility: NoteVisibility = NoteVisibility.public,
        visibility_users: List[Object] = [],
        local_only: bool = False,
    ) -> Note:
        data = {
            "visibility": visibility.value,
            "text": text,
            "visibleUserIds": [user.id for user in visibility_users],
            "localOnly": local_only,
        }
        return Note((await self._rest.create_note(data))["createdNote"])

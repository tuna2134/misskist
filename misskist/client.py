from __future__ import annotations
from .http import RestAPI
from .streaming import StreamingClient
from .enums import ChannelType

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .events import Channel

from asyncio import AbstractEventLoop


class Client:
    
    def __init__(self, endpoint: str, *, ssl: bool = True, loop: Optional[AbstractEventLoop] = None):
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

    async def connect(self, token: str):
        self._streaming = await StreamingClient.connect(self, token)
        self.loop.create_task(self.on_connect())
        await self._streaming.get_event_always()


    async def add_channel(self, channel: Channel):
        channel._inject(self)
        if not self._not_connected:
            await channel._connect()
            self.channels[channel.uid] = channel
        else:
            self._wait_channels.append(channel)
from __future__ import annotations
from .enums import ChannelType

from typing import TYPE_CHECKING
from inspect import iscoroutinefunction, getmembers
from functools import wraps

if TYPE_CHECKING:
    from .client import Client


class Channel:
    def __init_subclass__(cls, *, channel_type: ChannelType):
        cls.channel_type = channel_type
        cls.events = {}

    def _inject(self, client: Client):
        self.client = client
        for name, func in getmembers(self):
            if isinstance(func, EventFunction):
                print(func.event_name)
                func.event = self
                self.add_event(func.event_name, func)
    
    async def _connect(self):
        uid = await self.client._streaming.connect_channel(self.channel_type)
        self.uid = uid
        self.client.channels[uid] = self
    
    def dispatch(self, name: str, *args):
        for event in self.events.get(name, []):
            self.client.loop.create_task(event(*args))

    def add_event(self, name: str, func):
        if name not in self.events:
            self.events[name] = [func]
        else:
            self.events[name].append(func)


class EventFunction:
    def __init__(self, event_name: str, func):
        self.func = func
        self.event_name = event_name
    
    async def __call__(self, *args):
        await self.func(self.event, *args)


def on_event(event_name: str):
    def wrapper(func):
        return EventFunction("on_" + event_name, func)
    return wrapper
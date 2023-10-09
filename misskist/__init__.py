from .client import Client
from .enums import ChannelType
from .events import Channel, on_event


class Object:
    id: str

    def __init__(self, id: str):
        self.id = id


__all__ = (
    "Client",
    "Object",
    "ChannelType",
    "Channel",
    "on_event",
)
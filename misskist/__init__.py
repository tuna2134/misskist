from .client import Client
from .enums import ChannelType
from .events import Channel, on_event


class Object:
    id: str

    def __init__(self, id: str):
        self.id = id

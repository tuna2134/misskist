from enum import Enum


class ChannelType(Enum):
    global_timeline = 0


class NoteVisibility(Enum):
    public = "public"
    home = "home"
    followers = "followers"
    specified = "specified"

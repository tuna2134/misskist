from enum import Enum


class ChannelType(Enum):
    """
    チャンネルのタイプ
    
    Attributes
    ----------
    global_timeline:
        グローバルタイムライン
    """
    global_timeline = 0


class NoteVisibility(Enum):
    public = "public"
    home = "home"
    followers = "followers"
    specified = "specified"

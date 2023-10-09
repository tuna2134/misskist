from __future__ import annotations
from .http import RestAPI
from .streaming import StreamingClient
from .enums import ChannelType, NoteVisibility
from .note import Note

from typing import Optional, TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from .events import Channel

from asyncio import AbstractEventLoop


class Client:
    """Client
    
    Parameters
    ----------
    endpoint: :class:`str`
        Misskeyインスタンスのエンドポイント
    ssl: :class:`bool`
        SSLを使用するかどうか(デフォルトはTrue)
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        使用するイベントループ
    
    Attributes
    ----------
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        使用するイベントループ
    channels: Dict[:class:`str`, :class:`Channel`]
        チャンネル
    """
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
        self.channels: Dict[str, Channel] = {}
        self._wait_channels: List[Channel] = []

    async def on_connect(self) -> None:
        self._not_connected = False
        for channel in self._wait_channels:
            await channel._connect()
            self.channels[channel.uid] = channel

    def set_token(self, token: str) -> None:
        """
        トークンをセットします。
        
        Parameters
        ----------
        token: :class:`str`
            トークン
        """
        self._rest.token = token

    async def connect(self) -> None:
        """
        Misskeyのストリーミングに接続します。
        """
        self._streaming = await StreamingClient.connect(self)
        self.loop.create_task(self.on_connect())
        await self._streaming.get_event_always()

    async def start(self, token: str) -> None:
        self.set_token(token)
        await self.connect()

    async def add_channel(self, channel: Channel) -> None:
        """
        チャンネルイベントを追加します。基本的にイベントの受信はこれを使ってください。
        
        Parameters
        ----------
        channel: :class:`Channel`
            チャンネル
        """
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
        """
        ノートを投稿します。
        
        Parameters
        ----------
        text: Optional[:class:`str`]
            テキスト
        visibility: :class:`NoteVisivility`
            ノートを外部公開するかどうか
        visibility_users: List[:class:`Object`]
            ノートを公開する範囲を指定
        local_only: :class:`bool`
            misskeyのローカルでの公開
        """
        data = {
            "visibility": visibility.value,
            "text": text,
            "visibleUserIds": [user.id for user in visibility_users],
            "localOnly": local_only,
        }
        return Note((await self._rest.create_note(data))["createdNote"])

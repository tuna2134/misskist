from typing import Optional


class Note:
    """
    ノートの内容

    Attributes
    ----------
    id: :class:`str`
        ノートのID
    text: Optional[:class:`str`]
        ノートの内容
    """
    def __init__(self, data):
        self._data = data

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def text(self) -> Optional[str]:
        return self._data["text"]

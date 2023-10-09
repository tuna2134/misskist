from typing import Optional


class Note:
    def __init__(self, data):
        self.data = data

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def text(self) -> Optional[str]:
        return self.data["text"]

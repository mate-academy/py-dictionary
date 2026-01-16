import dataclasses
from typing import Any


@dataclasses.dataclass
class Item:
    key: Any
    value: Any
    hash_key: int


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.load_factor = 2 / 3
        self.raize = int(self.size * self.load_factor)
        self.item : list[Item] = [None] * self.size
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: str, value: Any) -> None:
        if self.length >= self.raize:
            self._resize()
        hash_key = hash(key)
        index = hash_key % self.size
        while self.item[index] is not None:
            if self.item[index].key == key:
                self.item[index].value = value
                return
            index = (index + 1) % self.size
        if self.item[index] is None:
            self.item[index] = Item(key, value, hash_key)
            self.length += 1

    def __getitem__(self, key: str) -> Any:
        hash_key = hash(key)
        index = hash_key % self.size
        while self.item[index] is not None:
            if self.item[index].key == key:
                return self.item[index].value
            index = (index + 1) % self.size
        raise KeyError(key)

    def _resize(self) -> None:
        old_item = [entry for entry in self.item if entry is not None]
        self.size *= 2
        self.raize = int(self.size * self.load_factor)
        self.item = [None] * self.size
        self.length = 0
        for entry in old_item:
            key = entry.key
            value = entry.value
            self[key] = value

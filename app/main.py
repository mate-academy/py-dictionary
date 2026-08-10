import dataclasses
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.slots = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.slots[index] is not None:
            if self.slots[index].key == key:
                self.slots[index].value = value
                return
            index = (index + 1) % self.capacity

        self.slots[index] = Node(key, value, key_hash)
        self.length += 1

        if self.length >= self.capacity * self.load_factor:
            self.resize()

    def resize(self) -> None:
        old_slots = self.slots
        self.capacity = self.capacity * 2
        self.slots = [None] * self.capacity
        self.length = 0
        for slot in old_slots:
            if slot is not None:
                self.__setitem__(slot.key, slot.value)

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.slots[index] is not None:
            if self.slots[index].key == key:
                return self.slots[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length


@dataclasses.dataclass
class Node:
    key: Any
    value: Any
    hash: int  # noqa: VNE003

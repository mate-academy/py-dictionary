from typing import Any


class Node:

    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:

    def __init__(self) -> None:
        self._capacity = 8
        self._table = [None] * self._capacity
        self._size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        index = h % self._capacity
        while True:
            slot = self._table[index]

            if slot is None:
                self._table[index] = Node(key, h, value)
                self._size += 1
                break

            if slot.key == key:
                slot.value = value
                return

            index = (index + 1) % self._capacity

        if self._size / self._capacity > 2 / 3:
            self.update_dict()

    def update_dict(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0
        for slot in old_table:
            if slot is not None:
                self[slot.key] = slot.value

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        index = h % self._capacity

        while True:
            slot = self._table[index]

            if slot is None:
                raise KeyError(key)

            if slot.key == key:
                return slot.value

            index = (index + 1) % self._capacity

    def __len__(self) -> int:
        return self._size

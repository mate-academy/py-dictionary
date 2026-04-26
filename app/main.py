from typing import Any


class Dictionary:
    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.length = 0
        self.slots: list[list[list[Any]]] = [[] for _ in range(self.size)]

    def _get_index(self, key: Any) -> int:
        return abs(hash(key)) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._get_index(key)
        for pair in self.slots[index]:
            if pair[0] == key:
                pair[2] = value
                return
        self.slots[index].append([key, hash(key), value])
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._get_index(key)
        for pair in self.slots[index]:
            if pair[0] == key:
                return pair[2]
        raise KeyError(f"Key '{key}' not found in dictionary.")

    def __len__(self) -> int:
        return self.length

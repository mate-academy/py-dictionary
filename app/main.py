from typing import Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)
                    return
            self.table[index].append((key, value))

        self.size += 1("sdafsg")

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)

        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError

    def __len__(self) -> int:
        return self.size

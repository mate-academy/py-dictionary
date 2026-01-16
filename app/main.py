from typing import Any, List, Optional


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.data: List[Optional[List[Any]]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        if not self.data[index]:
            self.data[index] = []
        for pair in self.data[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.data[index].append([key, value])
        self.size += 1
        if self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        if not self.data[index]:
            raise KeyError(f"Key {key} not found.")
        for pair in self.data[index]:
            if pair[0] == key:
                return pair[1]
        raise KeyError(f"Key {key} not found.")

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        if not self.data[index]:
            raise KeyError(f"Key {key} not found.")
        for i, pair in enumerate(self.data[index]):
            if pair[0] == key:
                del self.data[index][i]
                self.size -= 1
                return
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> Any:
        return self.size

    def _resize(self) -> None:
        old_data = self.data
        self.capacity *= 2
        self.size = 0
        self.data = [None] * self.capacity
        for bucket in old_data:
            if bucket:
                for key, value in bucket:
                    self[key] = value

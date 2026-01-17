from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]
        self.load_factor = 2 / 3

    def __hash_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if float(self.size / self.capacity) > self.load_factor:
            self._resize()

        index = self.__hash_index(key)
        box = self.table[index]
        for i, (k, v) in enumerate(box):
            if k == key:
                box[i] = (key, value)
                return
        box.append((key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        box = self.table[index]
        for (k, v) in box:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_table:
            for (k, v) in bucket:
                self[k] = v

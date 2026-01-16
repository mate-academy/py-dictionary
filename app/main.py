from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = int(self.capacity * (2 / 3))
        self.storage = [[] for _ in range(self.capacity)]
        print(self.storage)

    def resize_table(self) -> None:
        old_storage = self.storage
        self.capacity *= 2
        self.storage = [[] for _ in range(self.capacity)]
        self.load_factor = int(self.capacity * (2 / 3))
        self.size = 0
        for node in old_storage:
            if node and len(node) == 2:
                key, value = node
                self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size == self.load_factor:
            self.resize_table()

        _hash = hash(key) % self.capacity
        index = _hash

        while True:
            if self.storage[index] == [] or self.storage[index][0] == key:
                if not self.storage[index]:
                    self.size += 1
                self.storage[index] = [key, value]
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        _hash = hash(key) % self.capacity
        index = _hash

        while True:
            if self.storage[index] and self.storage[index][0] == key:
                return self.storage[index][1]

            index = (index + 1) % self.capacity

            if index == _hash:
                break

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

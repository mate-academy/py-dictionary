from typing import Hashable, Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.storage = [None] * self.capacity

    def resize(self) -> None:
        capacity_resized = self.capacity * 2
        storage_resized = [None] * capacity_resized
        for data in self.storage:
            if data:
                key, value = data
                index = hash(key) % capacity_resized
                while storage_resized[index]:
                    index = (index + 1) % capacity_resized
                storage_resized[index] = key, value
        self.storage = storage_resized
        self.capacity = capacity_resized

    def index_key(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.storage[index] is not None:
            existing_key, existing_value = self.storage[index]
            if existing_key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.index_key(key)
        if self.storage[index] is None:
            self.size += 1
        self.storage[index] = (key, value)
        if self.size >= self.capacity * (2 / 3):
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.index_key(key)
        if self.storage[index] is None:
            raise KeyError(f"Key {key} is not found")
        return self.storage[index][1]

    def __len__(self) -> int:
        return self.size

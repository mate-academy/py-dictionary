from typing import Any, Hashable


class Dictionary:
    INIT_CAPACITY = 8
    RESIZE_MULTIPLIER = 2
    THRESHOLD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INIT_CAPACITY
        self.size = 0
        self.data_storage = [None] * self.capacity

    def resize(self) -> None:
        capacity_upgrade = self.capacity * self.RESIZE_MULTIPLIER
        data_storage_upgrade = [None] * capacity_upgrade
        for data in self.data_storage:
            if data:
                key, value = data
                index = hash(key) % capacity_upgrade
                while data_storage_upgrade[index]:
                    index = (index + 1) % capacity_upgrade
                data_storage_upgrade[index] = (key, value)
        self.data_storage = data_storage_upgrade
        self.capacity = capacity_upgrade

    def index_key(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.data_storage[index] is not None:
            _key, _value = self.data_storage[index]
            if _key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.index_key(key)
        if self.data_storage[index] is None:
            self.size += 1
        self.data_storage[index] = (key, value)
        if self.size >= self.capacity * self.THRESHOLD_FACTOR:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.index_key(key)
        if self.data_storage[index] is None:
            raise KeyError
        return self.data_storage[index][1]

    def __len__(self) -> int:
        return self.size

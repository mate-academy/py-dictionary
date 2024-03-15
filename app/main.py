from typing import Any, Hashable


class Dictionary:

    def __init__(self,
                 capacity: int = 8,
                 load_factor: float = 0.75,
                 size: int = 0,
                 ) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = size
        self.hash_table = [None] * self.capacity

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [None] * self.capacity
        for bucket in self.hash_table:
            if bucket is not None:
                for key, value, hash_key in bucket:
                    index = hash_key % self.capacity
                    if new_hash_table[index] is None:
                        new_hash_table[index] = []
                    new_hash_table[index].append([key, value, hash_key])
        self.hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = []
        for i in self.hash_table[index]:
            if i[0] == key:
                i[1] = value
                return
        self.hash_table[index].append([key, value, hash(key)])
        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, item: Any) -> None:
        index = hash(item) % self.capacity
        if self.hash_table[index] is not None:
            for key, value, hash_key in self.hash_table[index]:
                if key == item:
                    return value
        raise KeyError(item)

    def __delitem__(self, item: Any) -> Any:
        index = hash(item) % self.capacity
        if self.hash_table[index] is not None:
            for i, (key, value, hash_key) in enumerate(
                    self.hash_table[index]):
                if item == key:
                    del self.hash_table[index][i]
                    return
            raise KeyError(item)

    def __iter__(self) -> None:
        for bucket in self.hash_table:
            if bucket is not None:
                for key, value, hash_key in bucket:
                    yield key

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0

    def get(self, key: Hashable, default_value: None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def pop(self, key: Hashable) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            raise KeyError(key)

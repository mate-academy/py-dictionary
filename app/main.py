from typing import Any


class Pair:
    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.buckets = [None] * self.capacity

    def resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        for item in old_buckets:
            if item is not None:
                index = item.hash % self.capacity
                while self.buckets[index] is not None:
                    index = (index + 1) % self.capacity
                self.buckets[index] = item

    def __setitem__(self, key: str, value: Any) -> None:
        if self.size == self.capacity:
            self.resize()
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                self.buckets[index].value = value
                return
            index = (index + 1) % self.capacity

        self.buckets[index] = Pair(key, value)
        self.size += 1

    def __getitem__(self, key: str) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                return self.buckets[index].value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key!r} not found")

    def __len__(self) -> int:
        return self.size

    def _rehash_from(self, start_index: int) -> None:
        index = (start_index + 1) % self.capacity
        while self.buckets[index] is not None:
            node = self.buckets[index]
            self.buckets[index] = None
            self.size -= 1
            self[node.key] = node.value
            index = (index + 1) % self.capacity

    def __delitem__(self, key: str) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                self.buckets[index] = None
                self.size -= 1
                self._rehash_from(index)
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key!r} not found")

    def pop(self, key: str, default: Any = None) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                value = self.buckets[index].value
                self.__delitem__(key)
                return value
            index = (index + 1) % self.capacity
        return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Any:
        for bucket in self.buckets:
            if bucket is not None:
                yield bucket.key

    def clear(self) -> None:
        for i in range(len(self.buckets)):
            self.buckets[i] = None
        self.size = 0

    def get(self, key: str, default: Any = None) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                return self.buckets[index].value
            index = (index + 1) % self.capacity
        return default

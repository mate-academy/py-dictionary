from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self._key = key
        self._value = value
        self._key_hash = key_hash


class Dictionary:
    def __init__(self) -> None:
        self.buckets = [[] for _ in range(8)]
        self.size = 0

    def _get_index(self, key: Any) -> int:
        index = hash(key) % len(self.buckets)
        return index

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / len(self.buckets) > 0.66:
            updated_buckets = [[] for _ in range(len(self.buckets) * 2)]
            for bucket in self.buckets:
                for node in bucket:
                    new_index = node._key_hash % len(updated_buckets)
                    updated_buckets[new_index].append(node)
            self.buckets = updated_buckets

        current_index = self._get_index(key)
        key_hash = hash(key)
        for node in self.buckets[current_index]:
            if node._key == key:
                node._value = value
                return
        self.buckets[current_index].append(Node(key, value, key_hash))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        current_index = self._get_index(key)
        for node in self.buckets[current_index]:
            if node._key == key:
                return node._value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

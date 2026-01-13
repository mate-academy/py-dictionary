from typing import Any

_sentinel = object()


class Dictionary:

    class Node:
        def __init__(self, key: Any, hash_key: int, value: Any) -> None:
            self.key = key
            self.hash_key = hash_key
            self.value = value

    def __init__(self) -> None:
        self.capacity: int = 8
        self.table: list[list[Dictionary.Node]] \
            = [[] for _ in range(self.capacity)]
        self.size: int = 0
        self.resize_threshold: float = 2 / 3
        self.keys_in_order: list[Any] = []

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.size + 1) / self.capacity >= self.resize_threshold:
            new_capacity = self.capacity * 2
            new_table = [[] for _ in range(new_capacity)]
            for bucket in self.table:
                for node in bucket:
                    new_index = node.hash_key % new_capacity
                    new_table[new_index].append(node)
            self.table = new_table
            self.capacity = new_capacity

        hash_key = hash(key)
        index = hash_key % self.capacity
        bucket = self.table[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Dictionary.Node(key, hash_key, value))
        self.size += 1
        self.keys_in_order.append(key)

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        for node in self.table[index]:
            if node.key == key:
                return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        self.keys_in_order.clear()

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        bucket = self.table[index]
        for node in bucket:
            if node.key == key:
                bucket.remove(node)
                self.size -= 1
                self.keys_in_order.remove(key)
                return
        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = _sentinel) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not _sentinel:
                return default
            else:
                raise KeyError(key)

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> Any:
        for key in self.keys_in_order:
            yield key

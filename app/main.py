from typing import Any, List, Hashable


class Node:
    def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.load_factor = load_factor
        self.capacity = initial_capacity
        self.size = 0
        self.hash_table: List[List[Node]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: Hashable) -> int:
        return hash(key)

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table: List[List[Node]] = [[] for _ in range(new_capacity)]

        for bucket in self.hash_table:
            for node in bucket:
                index = node.hash_value % new_capacity
                new_table[index].append(node)

        self.hash_table = new_table
        self.capacity = new_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        hash_value = self._hash(key)
        index = hash_value % self.capacity

        for node in self.hash_table[index]:
            if node.key == key:
                node.value = value
                return

        self.hash_table[index].append(Node(key, hash_value, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = self._hash(key)
        index = hash_value % self.capacity

        for node in self.hash_table[index]:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        hash_value = self._hash(key)
        index = hash_value % self.capacity

        for i, node in enumerate(self.hash_table[index]):
            if node.key == key:
                del self.hash_table[index][i]
                self.size -= 1
                return

        raise KeyError(f"Key {key} not found")

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is None:
                raise
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Any:
        for bucket in self.hash_table:
            for node in bucket:
                yield node.key

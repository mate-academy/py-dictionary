from typing import Any, List


class Node:
    def __init__(self, key: Any, hash_: int, value: Any) -> None:
        self.key = key
        self.hash = hash_
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.table: List[List[Node]] = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        for node in self.table[index]:
            if node.key == key and node.hash == hash_value:
                node.value = value
                return

        self.table[index].append(Node(key, hash_value, value))
        self.size += 1

        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        for node in self.table[index]:
            if node.key == key and node.hash == hash_value:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity *= 2
        new_table: List[List[Node]] = [[] for _ in range(self.capacity)]

        for bucket in self.table:
            for node in bucket:
                index: int = node.hash % self.capacity
                new_table[index].append(node)

        self.table = new_table

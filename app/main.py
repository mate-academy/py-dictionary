from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.length = 0
        self.table: list[Node | None] = [None] * self.capacity
        self.load_factor = 2 / 3

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key: Any, hash_value: int) -> int:
        index = hash_value % self.capacity

        while self.table[index] is not None:
            node = self.table[index]
            if node.hash == hash_value and node.key == key:
                return index

            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.load_factor:
            self._resize()

        hash_value = hash(key)
        index = self._get_index(key, hash_value)

        if self.table[index] is None:
            self.table[index] = Node(key, value, hash_value)
            self.length += 1
        else:
            self.table[index].value = value

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = self._get_index(key, hash_value)

        node = self.table[index]
        if node is None:
            raise KeyError(key)

        return node.value

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def get(self, key: Any, default: Any = None) -> Any:
        hash_value = hash(key)
        index = self._get_index(key, hash_value)
        node = self.table[index]
        return node.value if node is not None else default

    def clear(self) -> None:
        self.capacity = 8
        self.length = 0
        self.table = [None] * self.capacity

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for node in self.table:
            if node is not None:
                yield node.key

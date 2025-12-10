from typing import Any, Optional


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __repr__(self) -> str:
        return f"Node({self.key}, {self.value})"


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.table: list[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def _find_slot(self, key: Any, hash_code: int) -> int:
        index = hash_code % self.capacity

        while True:
            cell = self.table[index]
            if cell is None:
                return index

            if cell.hash == hash_code and cell.key == key:
                return index

            index = (index + 1) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_code = hash(key)

        if (self.length + 1) / self.capacity > self.LOAD_FACTOR:
            self._resize()

        index = self._find_slot(key, hash_code)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.length += 1
        else:
            self.table[index].value = value

    def __getitem__(self, key: Any) -> Any:
        hash_code = hash(key)
        index = hash_code % self.capacity

        while True:
            cell = self.table[index]
            if cell is None:
                raise KeyError(f"Key not founds: {key}")

            if cell.hash == hash_code and cell.key == key:
                return cell.value

            index = (index + 1) % self.capacity

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.length = 0

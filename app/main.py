from typing import Any


class Node:
    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.length = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def _get_index(self, hash_value: int) -> int:
        return hash_value % self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)

        while self.hash_table[index] is not None:
            existing_node = self.hash_table[index]
            if existing_node.hash == key_hash and existing_node.key == key:
                existing_node.value = value
                return
            index = (index + 1) % self.capacity

        if (self.length + 1) > self.capacity * self.LOAD_FACTOR:
            self._resize()
            self[key] = value
            return

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        start_index = index

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == key_hash and node.key == key:
                return node.value
            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(f"Key not found: {key!r}")

    def __len__(self) -> int:
        return self.length

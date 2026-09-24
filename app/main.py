from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(self.key)


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.7) -> None:
        self.length = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        node = Node(key, value)
        place_in_table = node.hash % self.capacity

        while self.hash_table[place_in_table] is not None:
            if self.hash_table[place_in_table].key == key:
                self.hash_table[place_in_table].value = value
                return
            place_in_table = (place_in_table + 1) % self.capacity

        self.hash_table[place_in_table] = node
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        node_hash = hash(key)
        place_in_table = node_hash % self.capacity
        start_index = place_in_table

        while self.hash_table[place_in_table] is not None:
            if self.hash_table[place_in_table].key == key:
                return self.hash_table[place_in_table].value
            place_in_table = (place_in_table + 1) % self.capacity
            if place_in_table == start_index:
                break

        raise KeyError(f"Key {key!r} not found")

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        node_hash = hash(key)
        place_in_table = node_hash % self.capacity
        start_index = place_in_table

        while self.hash_table[place_in_table] is not None:
            if self.hash_table[place_in_table].key == key:
                value = self.hash_table[place_in_table].value
                self.hash_table[place_in_table] = None
                self.length -= 1
                return value
            place_in_table = (place_in_table + 1) % self.capacity
            if place_in_table == start_index:
                break

        raise KeyError(f"Key {key!r} not found")

    def update(self, other: dict) -> None:
        for k, v in other.items():
            self[k] = v

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for old_node in old_table:
            if old_node is not None:
                self[old_node.key] = old_node.value

from typing import Any


class Node:
    def __init__(self, value: Any, key: Any, hash_value: int) -> None:
        self.value = value
        self.key = key
        self.hash_value = hash_value


class Dictionary:
    def __init__(self) -> None:
        self.store = [None] * 8
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        old = self.store
        self.store = [None] * (len(old) * 2)
        self.length = 0
        for node in old:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        slot = hash_value % len(self.store)
        thing = Node(value, key, hash_value)
        while self.store[slot] is not None and self.store[slot].key != key:
            slot = (slot + 1) % len(self.store)
        if self.store[slot] is None:
            self.store[slot] = thing
            self.length += 1
            if self.length > 2 / 3 * len(self.store):
                self.resize()
        elif self.store[slot].key == key:
            self.store[slot].value = value

    def __getitem__(self, key: Any) -> Any:
        slot = hash(key) % len(self.store)
        while self.store[slot] is not None:
            if self.store[slot].key == key:
                return self.store[slot].value
            slot = (slot + 1) % len(self.store)
        raise KeyError(f"Key was not found {key}")

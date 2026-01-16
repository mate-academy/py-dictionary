from typing import Any


class Node:
    def __init__(self, key: Any, hash_val: int, value: Any) -> None:
        self.key = key
        self.hash_val = hash_val
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.table = [None] * size
        self.count = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_val = hash(key)
        index = hash_val % self.size
        node = self.table[index]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
        new_node = Node(key, hash_val, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.count += 1
        if self.count > self.size * 2:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_val = hash(key)
        index = hash_val % self.size
        node = self.table[index]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.count

    def __contains__(self, key: Any) -> bool:
        return bool(self.get(key))

    def __delitem__(self, key: Any) -> None:
        hash_val = hash(key)
        index = hash_val % self.size
        node = self.table[index]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self.table[index] = node.next
                else:
                    prev.next = node.next
                self.count -= 1
                return
            prev = node
            node = node.next
        raise KeyError(key)

    def clear(self) -> None:
        self.table = [None] * self.size
        self.count = 0

    def get(self, key: Any, default: Any = None) -> Any:
        return self.get(key, default)

    def pop(self, key: Any, default: Any = None) -> Any:
        value = self.get(key, default)
        if key in self:
            del self[key]
        return value

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for node in self.table:
            while node is not None:
                yield node.key
                node = node.next

    def _resize(self) -> None:
        self.size *= 2
        new_table = [None] * self.size
        for i in range(len(self.table)):
            node = self.table[i]
            while node is not None:
                next_node = node.next
                index = node.hash_val % self.size
                node.next = new_table[index]
                new_table[index] = node
                node = next_node
        self.table = new_table

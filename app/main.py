from typing import Any, Iterable, Tuple, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        node = self.hash_table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        if not self.hash_table[index]:
            self.hash_table[index] = Node(key, value)
        else:
            node = self.hash_table[index]
            while node:
                if node.key == key:
                    node.value = value
                    return
                if not node.next:
                    break
                node = node.next
            node.next = Node(key, value)
        self.length += 1
        if self.length >= self.load_factor * self.capacity:
            self._resize()

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        node = self.hash_table[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.hash_table[index] = node.next
                self.length -= 1
                return
            prev = node
            node = node.next
        raise KeyError(key)

    def __iter__(self) -> Iterable:
        for node in self.hash_table:
            while node:
                yield node.key
                node = node.next

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for node in self.hash_table:
            while node:
                index = hash(node.key) % new_capacity
                if not new_table[index]:
                    new_table[index] = Node(node.key, node.value)
                else:
                    current = new_table[index]
                    while current.next:
                        current = current.next
                    current.next = Node(node.key, node.value)
                node = node.next
        self.capacity = new_capacity
        self.hash_table = new_table

    def clear(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * self.capacity

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
            return default

    def update(self, other: Iterable[Tuple[Any, Any]]) -> None:
        for key, value in other:
            self[key] = value

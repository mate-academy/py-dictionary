from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next = None


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            while node:
                self.__setitem__(node.key, node.value)
                node = node.next

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash(key)
        node = self.hash_table[index]

        if node is None:
            self.hash_table[index] = Node(key, value)
            self.size += 1
        else:
            prev = None
            while node:
                if node.key == key:
                    node.value = value
                    return
                prev = node
                node = node.next

            prev.next = Node(key, value)
            self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> int:
        index = self._hash(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"{key} missing in dictionary")

    def __delitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        node = self.hash_table[index]
        prev = None

        while node:
            if node.key == key:
                if prev is None:
                    self.hash_table[index] = node.next
                else:
                    prev.next = node.next
                self.size -= 1
                return
            prev = node
            node = node.next

        raise KeyError(f"{key} missing in dictionary")

    def __contains__(self, key: Hashable) -> bool:
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __iter__(self) -> None:
        for node in self.hash_table:
            while node:
                yield node.key, node.value
                node = node.next

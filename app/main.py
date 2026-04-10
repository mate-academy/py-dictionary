from typing import Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.hash_table: list = [None] * capacity
        self.length = 0
        self.capacity = capacity

    def resize(self) -> None:
        self.capacity *= 2
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0
        for item in old_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * 2 // 3:
            self.resize()

        element = Node(key, value)
        index = element._hash % self.capacity

        for _ in range(self.capacity):
            if index == len(self.hash_table):
                index = 0

            if self.hash_table[index] is None:
                self.length += 1
                self.hash_table[index] = element
                return

            if self.hash_table[index].key == key:
                self.hash_table[index] = element
                return

            index += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        for _ in range(self.capacity):
            if index == len(self.hash_table):
                index = 0

            if self.hash_table[index] is None:
                raise KeyError

            if (self.hash_table[index]._hash == hash(key)
                    and self.hash_table[index].key == key):
                return self.hash_table[index].value

            index += 1

        raise KeyError

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity

        for _ in range(self.capacity):
            if index == len(self.hash_table):
                index = 0

            if self.hash_table[index] is not None:
                if (self.hash_table[index]._hash == hash(key)
                        and self.hash_table[index].key == key):
                    self.hash_table[index] = None
                    self.length -= 1
                    return

            index += 1

        raise KeyError


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self._hash = hash(key)
        self.key = key
        self.value = value

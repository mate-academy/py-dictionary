from typing import Any

INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 2 / 3


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.value = value
        self.key = key
        self.hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self._hashtable: list[None | Node] = [None] * self.capacity

    def calculate_index(self, key: Any) -> int:
        index = hash(key) % self.capacity
        while (
                self._hashtable[index] is not None
                and self._hashtable[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_hash_table = self._hashtable
        self.capacity = self.capacity * 2
        self.size = 0
        self._hashtable: list[None | Node] = [None] * self.capacity

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self.calculate_index(key)

        if self._hashtable[index] is None:
            if self.size + 1 > self.capacity * RESIZE_THRESHOLD:
                self._resize()
                self.__setitem__(key, value)
                return

            self.size += 1

        self._hashtable[index] = Node(key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self.calculate_index(key)

        if self._hashtable[index] is None:
            raise KeyError(f"key {key} is not present in dictionary")

        return self._hashtable[index].value

    def __len__(self) -> int:
        return self.size

from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, hash_key: int, value: Any) -> None:
        self.key = key
        self.hash_key = hash_key
        self.value = value

    def __eq__(self, other: object) -> bool:
        return self.key == other.key and self.hash_key == other.hash_key


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None for _ in range(8)]
        self.current_size = 0
        self.capacity = len(self.hash_table)

    def __setitem__(self, key: Hashable, value: Any) -> None:

        threshold = int(0.66 * self.capacity)
        node = Node(key, hash(key), value)

        if self.current_size + 1 > threshold:
            self.__resize_hash_table()

        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = node
                self.current_size += 1
                break
            elif self.hash_table[index] == node:
                self.hash_table[index] = node
                break
            index = (index + 1) % self.capacity

    def __resize_hash_table(self) -> None:
        old_hash_table = [node for node in self.hash_table if node is not None]
        self.hash_table = [None for _ in range(self.capacity * 2)]
        self.capacity = len(self.hash_table)
        self.current_size = 0
        self.update(old_hash_table)

    def __getitem__(self, key: Hashable) -> Any:
        for el in self.hash_table:
            if el and el.key == key and el.hash_key == hash(key):
                return el.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.current_size

    def clear(self) -> None:
        self.hash_table = [None for _ in range(len(self.hash_table))]

    def __delitem__(self, key: Hashable) -> None:
        for i, el in enumerate(self.hash_table):
            if el and el.key == key:
                self.hash_table[i] = None
        raise KeyError(key)

    def get(self, key: Hashable, default_value: Any = "some value") -> Any:
        try:
            self.__getitem__(key)
        except KeyError:
            return default_value

    def pop(self, key: Hashable) -> Any:
        value = self.__getitem__(key)
        self.__delitem__(key)
        return Node(key, hash(key), value)

    def update(self, other: list[Node]) -> None:
        for node in other:
            self.__setitem__(node.key, node.value)

    def __iter__(self) -> object:
        self.current_element = 0
        return self

    def __next__(self) -> Any:
        if self.current_element >= self.current_size:
            raise StopIteration

        result = self.hash_table[self.current_element]
        self.current_element += 1
        return result

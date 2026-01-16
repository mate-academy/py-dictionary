from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = self.capacity * 0.67
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.load_factor:
            self.resize()

        node = Node(key, value)
        index = node.hash_key % self.capacity

        for item in self.hash_table:
            if item is not None:
                if item.key == key and item.hash_key == hash(key):
                    item.value = value
                    return

        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = node
                self.size += 1
                break
            elif index == self.capacity - 1:
                index = 0
            else:
                index += 1

    def __getitem__(self, key: Hashable) -> Any:
        for item in self.hash_table:
            if item is not None:
                if item.key == key and item.hash_key == hash(key):
                    return item.value

        raise KeyError(f"Invalid key: {key}")

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        prev_hash_table = self.hash_table
        self.capacity *= 2
        self.load_factor = self.capacity * 0.67
        self.hash_table = [None] * self.capacity
        self.size = 0
        for item in prev_hash_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def clear(self) -> None:
        self.__init__()

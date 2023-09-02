from typing import Hashable, Any


# Class where we save pairs : key/value + key hash
class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        # Checking the need for resize
        if self.size == self.threshold:
            self.resize()

        node = Node(key, value)
        index = node.hash_key % self.capacity
        # Check the presence of a key in the hash
        for item in self.hash_table:
            if item is not None:
                if item.hash_key == hash(key) and item.key == key:
                    item.value = value
                    return
        # Fill the cell of the hash table
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = node
                self.size += 1
                break
            elif index == self.capacity - 1:
                index = 0
            else:
                index += 1

    def __getitem__(self, item: Any) -> Any:
        for node in self.hash_table:
            if node is not None:
                if node.key == item:
                    return node.value

        raise KeyError(f"There is not item with key: {item}")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        for item in self.hash_table:
            if item is not None:
                if item.key == key:
                    self.hash_table[self.hash_table.index(item)] = None

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.size = 0
        self.hash_table = [None] * self.capacity
        # Reset objects in the hash table
        for item in old_hash_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Any) -> Any:
        return self.__getitem__(key)

    def pop(self, key: Any) -> Any:
        value = self.get(key)
        self.__delitem__(key)
        return value

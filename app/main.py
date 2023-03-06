from typing import Hashable, Any

CAPACITY = 8


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash(key)


class Dictionary:
    def __init__(self, capacity: int = CAPACITY) -> None:
        self.capacity = capacity
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity
        self.size = 0

    def calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = self.cyclic_increment(index)

        return index

    def cyclic_increment(self, index: int) -> int:
        return (index + 1) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.load_factor * self.capacity:
            self.resize()

        index = self.calculate_index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, value)
            self.size += 1
        else:
            if self.hash_table[index].key == key:
                self.hash_table[index] = Node(key, value)
            else:
                index = self.calculate_index(key)

                if self.hash_table[index] is None:
                    self.hash_table[index] = Node(key, value)
                    self.size += 1

                    if self.size > self.capacity * self.load_factor:
                        self.resize()
                else:
                    self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self.hash_table[index].value

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.__init__(self.capacity * 2)

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __len__(self) -> int:
        return self.size

from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any, hash_num: int) -> None:
        self.key = key
        self.value = value
        self.hash_num = hash_num


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.threshold = 2 / 3
        self.length = 0

    def _find_index(self, key: Hashable, hash_num: int) -> int:
        index = hash_num % self.capacity
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            assert node is not None
            if node.hash_num == hash_num and node.key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_num = hash(key)
        index = self._find_index(key, hash_num)
        node = self.hash_table[index]

        if node is not None:
            node.value = value
            return

        self.hash_table[index] = Node(key, value, hash_num)
        self.length += 1
        self.resize_and_rehash_if_necessary()

    def __getitem__(self, key: Hashable) -> Any:
        hash_num = hash(key)
        index = self._find_index(key, hash_num)
        node = self.hash_table[index]
        if node is None:
            raise KeyError(key)
        assert node is not None
        return node.value

    def __len__(self) -> int:
        return self.length

    def resize_and_rehash_if_necessary(self) -> None:
        if self.length <= self.capacity * self.threshold:
            return
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                index = node.hash_num % self.capacity
                while self.hash_table[index] is not None:
                    index = (index + 1) % self.capacity
                self.hash_table[index] = node

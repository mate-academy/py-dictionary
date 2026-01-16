from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.max_capacity = 8
        self.threshold = int(self.max_capacity * 0.7)
        self.current_capacity = 0
        self.enlarger = 2
        self.table = [None] * self.max_capacity

    @staticmethod
    def _hash(key: Any) -> int:
        hash_value = 0
        key_str = repr(key)
        for index, char in enumerate(key_str):
            hash_value = (hash_value * 7 + ord(char))
        return hash_value

    def get_index(self, key: Any) -> int:
        # print(f"index {self.get_hash(key) % self.max_capacity}")
        return self._hash(key) % self.max_capacity

    def insert(self, index: int, key: Any, value: Any) -> None:
        self.table[index] = Node(key, value)
        # print(f"Key {key}")
        self.current_capacity += 1

    def rebuild_table(self) -> None:
        self.max_capacity *= self.enlarger
        self.threshold = int(self.max_capacity * 0.7)
        old_table = self.table
        self.table = [None] * self.max_capacity
        self.current_capacity = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.current_capacity >= self.threshold:
            self.rebuild_table()

        index = self.get_index(key)

        while True:
            if self.table[index] is None:
                self.insert(index, key, value)
                break
            elif self.table[index].key == key:
                self.table[index].value = value
                break
            index += 1
            if index == self.max_capacity:
                index = 0

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key)
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.max_capacity
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.current_capacity

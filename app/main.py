from typing import List, Optional, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: List[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] and (
                self.hash_table[index].key != key
                or hash(self.hash_table[index].key) != hash_value
        ):
            index = (index + 1) % self.capacity

        if self.hash_table[index]:
            self.hash_table[index].value = value
        else:
            self.hash_table[index] = Node(key, hash_value, value)
            self.length += 1

        if self.length / self.capacity > self.load_factor:
            self._resize(self.capacity * 2)

    def __getitem__(self, key: Any) -> Optional[Any]:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] and self.hash_table[index].key != key:
            index = (index + 1) % self.capacity

        if self.hash_table[index]:
            return self.hash_table[index].value

        raise KeyError(key)

    def _resize(self, new_capacity: int) -> None:
        new_table = [None] * new_capacity

        for node in self.hash_table:
            if node:
                index = hash(node.key) % new_capacity
                while new_table[index] is not None:
                    index = (index + 1) % new_capacity
                new_table.__setitem__(index, node)  # type: ignore

        self.capacity = new_capacity
        self.hash_table = new_table

    def __len__(self) -> int:
        return self.length


class Node:
    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value

    def __hash__(self) -> Any:
        return hash(self.key)

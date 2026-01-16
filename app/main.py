from typing import Any, List, Optional, Hashable


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 16,
            load_factor: float = 0.75
    ) -> None:
        self.initial_capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.table: List[Optional[List[List[Any]]]] = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.load_factor * self.capacity:
            self._resize()
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity
        if self.table[index] is None:
            self.table[index] = []
        for node in self.table[index]:
            if node[0] == key:
                node[2] = value
                return
        self.table[index].append([key, hash_value, value])
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity
        if self.table[index] is not None:
            for node in self.table[index]:
                if node[0] == key:
                    return node[2]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity *= 2
        new_table: List[Optional[List[List[Any]]]] = [None] * self.capacity
        for index in range(len(self.table)):
            if self.table[index] is not None:
                for node in self.table[index]:
                    new_index: int = node[1] % self.capacity
                    if new_table[new_index] is None:
                        new_table[new_index] = []
                    new_table[new_index].append(node)
        self.table = new_table

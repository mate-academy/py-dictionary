from typing import Any, List, Optional, Tuple
DictNode = Optional[Tuple[Any, int, Any]]


class Dictionary:
    pass
    LOAD_FACTOR_THRESHOLD = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.table: List[DictNode] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, key_hash, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        start_index = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][2]
            index = (index + 1) % self.capacity

            if index == start_index:
                break

        raise KeyError(f"Key '{key}' not found in Dictionary.")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                key, key_hash, value = node
                self.__setitem__(key, value)

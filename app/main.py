from typing import Any, Optional


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.length: int = 0
        self.table: list[Optional[tuple]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self.capacity > 0.66:
            self._resize()

        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            current_item = self.table[index]

            if current_item is not None and current_item[0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        initial_index = index

        while self.table[index] is not None:
            current_item = self.table[index]
            if current_item is not None and current_item[0] == key:
                return current_item[1]

            index = (index + 1) % self.capacity
            if index == initial_index:
                break

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for item in old_table:
            if item is not None:
                self.__setitem__(item[0], item[1])

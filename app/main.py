from typing import Any, Hashable


class Dictionary:
    def __init__(self, load_factor: float = 0.75, capacity: int = 8) -> None:
        self.size = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hashed = hash(key)
        threshold = int(self.capacity * self.load_factor)
        if self.size == threshold:
            self.resize()
        index = hashed % self.capacity
        for item in range(self.capacity):
            current_index = (index + item) % self.capacity
            if not self.table[current_index]:
                self.table[current_index] = [key, value, hashed]
                self.size += 1
                break
            if (
                key == self.table[current_index][0]
                and hashed == self.table[current_index][2]
            ):
                self.table[current_index][1] = value
                break

    def __getitem__(self, key: Hashable) -> Any:
        hashed = hash(key)
        index = hashed % self.capacity
        for item in range(self.capacity):
            current_index = (index + item) % self.capacity
            if not self.table[current_index]:
                break
            if (
                self.table[current_index][0] == key
                and self.table[current_index][2] == hashed
            ):
                return self.table[current_index][1]
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        new_copy = self.table
        self.size = 0
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        for item in new_copy:
            if item:
                self.__setitem__(item[0], item[1])

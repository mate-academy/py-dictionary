from typing import Any


class Pair:
    def __init__(self, key: int, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = 0.6
        self.cell_count = 0
        self.hashtable = [None] * self.capacity

    def __setitem__(self, key: int, value: Any) -> Any:
        index = hash(key) % self.capacity
        while self.hashtable[index] is not None:
            if self.hashtable[index].key == key:
                self.hashtable[index].value = value
                return value
            index = (index + 1) % self.capacity
        self.hashtable[index] = Pair(key, value)
        self.cell_count += 1
        if self.cell_count > (self.threshold * self.capacity):
            self.resize()

    def resize(self) -> None:
        current_cell = [cell for cell in self.hashtable if cell is not None]
        self.capacity *= 2
        self.hashtable = [None] * self.capacity
        self.cell_count = 0
        for cell in current_cell:
            self.__setitem__(cell.key, cell.value)

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.hashtable[index] is not None:
            if self.hashtable[index].key == key:
                return self.hashtable[index].value
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.cell_count

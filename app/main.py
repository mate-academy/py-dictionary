from dataclasses import dataclass
from typing import Any


@dataclass
class Cell:
    key: Any
    hash_f: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size > self.capacity * 2 // 3:
            self._resize()

        h = hash(key)
        index = h % self.capacity

        for _ in range(self.capacity):
            cell = self.table[index]

            if cell is None:
                self.table[index] = Cell(key, h, value)
                self.size += 1
                return
            elif cell.key == key:
                self.table[index].value = value
                return
            else:
                index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        index = h % self.capacity

        for _ in range(self.capacity):
            cell = self.table[index]

            if cell is None:
                raise KeyError(key)
            elif cell.key == key:
                return cell.value
            else:
                index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for cell in old_table:
            if cell is not None:
                self.__setitem__(cell.key, cell.value)

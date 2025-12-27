from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, length: int = 0) -> None:
        self.capacity = capacity
        self.length = length
        self.threshold = int(self.capacity * 2 / 3) + 1
        self.cells = [None for _ in range(self.capacity)]

    def resize_cells(self) -> None:
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3) + 1
        old_cells = self.cells
        self.cells = [None for _ in range(self.capacity)]
        for cell in old_cells:
            if cell:
                self.__setitem__(cell[0], cell[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length >= self.threshold:
            self.resize_cells()
        index = hash(key) % self.capacity
        while True:
            if self.cells[index] is None:
                self.cells[index] = [key, value]
                self.length += 1
                break
            if self.cells[index][0] == key:
                self.cells[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, input_key: Hashable) -> None:
        index = hash(input_key) % self.capacity
        while True:
            if self.cells[index]:
                if self.cells[index][0] == input_key:
                    return self.cells[index][1]
            else:
                raise KeyError
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

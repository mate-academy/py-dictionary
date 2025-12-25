from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.hash_table: list = [[] for _ in range(self.capacity)]
        self.cells_occupied: int = 0

    def __getitem__(
            self,
            key: Any
    ) -> Any:
        cell = hash(key) % self.capacity
        for _ in range(self.capacity):
            if self.hash_table[cell] and self.hash_table[cell][0] == key:
                return self.hash_table[cell][2]
            else:
                cell = (cell + 1) % self.capacity
        raise KeyError

    def __setitem__(
            self,
            key: Any,
            value: Any
    ) -> None:
        if self.cells_occupied >= round(self.capacity * (2 / 3)):
            self.resize()
        cell_number = hash(key) % self.capacity
        while True:
            if not self.hash_table[cell_number]:
                self.hash_table[cell_number] = [key, hash(key), value]
                self.cells_occupied += 1
                break
            elif self.hash_table[cell_number][0] == key:
                self.hash_table[cell_number][2] = value
                break
            else:
                cell_number = (cell_number + 1) % self.capacity

    def resize(self) -> None:
        self.cells_occupied = 0
        self.capacity *= 2
        previous_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for cell in previous_table:
            if cell:
                self.__setitem__(cell[0], cell[2])

    def __len__(self) -> int:
        return self.cells_occupied

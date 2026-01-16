from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.cell = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        cell = self.cell[index]

        for i, (k, v) in enumerate(cell):
            if k == key:
                cell[i] = (key, value)
                return
        cell.append((key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_cell = [[] for _ in range(new_capacity)]

        for cell in self.cell:
            for key, value in cell:
                index = hash(key) % new_capacity
                new_cell[index].append((key, value))

        self.capacity = new_capacity
        self.cell = new_cell

    def __getitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        cell = self.cell[index]

        for k, v in cell:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

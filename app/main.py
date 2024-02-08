from typing import Hashable, Any


class Dictionary:

    def __init__(
            self,
            capacity: int = 8,
            fill_percent: float = 0.66,
    ) -> None:
        self.capacity = capacity
        self.fill_percent = fill_percent
        self.size = 0
        self.hash_table = [[] for _ in range(capacity)]

    def _hash_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [[] for _ in range(self.capacity)]

        for cells in self.hash_table:
            for cell in cells:
                index = self._hash_index(cell[0])
                new_hash_table[index].append(cell)

        self.hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash_index(key)

        for cell in self.hash_table[index]:
            if cell[0] == key:
                cell[1] = value
                return

        self.hash_table[index].append([key, value])
        self.size += 1

        if self.size / self.capacity >= self.fill_percent:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash_index(key)
        for cell in self.hash_table[index]:
            if cell[0] == key:
                return cell[1]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

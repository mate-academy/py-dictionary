from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity

    def need_to_resize(self) -> int:
        return self.size / self.capacity > 0.7

    def _get_index_(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> Any:
        old_table = self.table.copy()
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for cell in old_table:
            if cell is not None:
                for (key, value, hash_of_key) in cell:
                    self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_of_key = hash(key)
        index_of_cell = self._get_index_(key)

        if self.table[index_of_cell] is None:
            self.table[index_of_cell] = [(key, value, hash_of_key)]
            self.size += 1
            return

        for i, (k, v, h) in enumerate(self.table[index_of_cell]):
            if key == k:
                self.table[index_of_cell][i] = (key, value, hash_of_key)
                return
        self.table[index_of_cell].append((key, value, hash_of_key))
        self.size += 1

        if self.need_to_resize():
            self._resize()

    def __getitem__(self, key: Any) -> None:
        hash(key)
        index_of_cell = self._get_index_(key)
        if self.table[index_of_cell] is None:
            raise KeyError(f"Key: {key} not found")
        else:
            for i, (k, v, h) in enumerate(self.table[index_of_cell]):
                if key == k:
                    return v
            raise KeyError(f"Key: {key} are different")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> Any:
        self.table = [None] * self.capacity
        self.size = 0

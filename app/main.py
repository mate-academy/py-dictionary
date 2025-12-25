from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self._cells = [None] * 8
        self.capacity = len(self._cells)
        self._threshold = 2 / 3 * self.capacity
        self.length = 0
        self._tombstone = object()

    def resize(self) -> None:
        new_cells = [None] * (self.capacity * 2)
        new_cells_threshold = 2 / 3 * len(new_cells)

        for cell in self._cells:
            if cell is not None and cell is not self._tombstone:
                new_id = cell[1] % len(new_cells)
                while new_cells[new_id] is not None:
                    new_id = (new_id + 1) % len(new_cells)
                new_cells[new_id] = cell

        self._cells = new_cells
        self.capacity = len(self._cells)
        self._threshold = new_cells_threshold

    def __setitem__(self, key: str | int, value: Any) -> None:
        if self.length >= self._threshold:
            self.resize()

        key_hash = hash(key)
        cell_index = key_hash % len(self._cells)
        while True:
            if (self._cells[cell_index] is None
                    or self._cells[cell_index] is self._tombstone):
                self._cells[cell_index] = (key, key_hash, value)
                self.length += 1
                break
            elif self._cells[cell_index][0] == key:
                self._cells[cell_index] = (key, key_hash, value)
                break
            else:
                cell_index = (cell_index + 1) % len(self._cells)

    def __getitem__(self, key: str | int) -> object:
        cell_index = hash(key) % len(self._cells)
        while True:
            if self._cells[cell_index] is None:
                raise KeyError(f"Key {key} not found")

            elif self._cells[cell_index] is self._tombstone:
                cell_index = (cell_index + 1) % len(self._cells)

            elif self._cells[cell_index][0] == key:
                return self._cells[cell_index][2]
            else:
                cell_index = (cell_index + 1) % len(self._cells)

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: str | int) -> None:
        cell_index = hash(key) % len(self._cells)
        while True:
            if self._cells[cell_index] is None:
                raise KeyError(f"Key {key} not found")

            elif self._cells[cell_index] is self._tombstone:
                cell_index = (cell_index + 1) % len(self._cells)

            elif self._cells[cell_index][0] == key:
                self._cells[cell_index] = self._tombstone
                self.length -= 1
                break

            else:
                cell_index = (cell_index + 1) % len(self._cells)

    def keys(self) -> Any:
        return (cell[0] for cell in self._cells
                if cell is not None and cell is not self._tombstone)

    def values(self) -> Any:
        return (cell[2] for cell in self._cells
                if cell is not None and cell is not self._tombstone)

    def items(self) -> Any:
        return ((cell[0], cell[2]) for cell in self._cells
                if cell is not None and cell is not self._tombstone)

    def update(self, dictionary: dict) -> None:

        for key, value in dictionary.items():
            self.__setitem__(key, value)

    def get(self, key: str | int, default : Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: str | int, default: Any = None) -> Any:
        try:
            return_value = self.__getitem__(key)
            self.__delitem__(key)
            return return_value
        except KeyError:
            return default

    def clear(self) -> None:
        self._cells = [None] * 8
        self.capacity = len(self._cells)
        self._threshold = 2 / 3 * self.capacity
        self.length = 0

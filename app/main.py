from typing import Any, Iterable


class Dictionary:
    def __init__(self, length: int = 8, load_factor: float = 2 / 3) -> None:
        self.initial_length = length
        self.length = length
        self.load_factor = load_factor
        self.hash_table = [[] for _ in range(self.length)]

    def __setitem__(self, key: Any, value: Any) -> None:
        if len(self) == int(self.length * self.load_factor):
            self._resize()

        key_index, hashed_key, empty = self.find_key_index(key)
        if empty:
            self.hash_table[key_index].extend([key, hashed_key, value])
        else:
            self.hash_table[key_index][2] = value

    def __getitem__(self, key: Any) -> Any:
        key_index, _, empty = self.find_key_index(key)
        if not empty:
            return self.hash_table[key_index][2]

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return sum(1 for cell in self.hash_table if cell)

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.length *= 2
        self.hash_table = [[] for _ in range(self.length)]
        for cell in old_hash_table:
            if cell:
                key_index = cell[1] % self.length
                while self.hash_table[key_index]:
                    key_index = (key_index + 1) % self.length
                self.hash_table[key_index].extend([cell[0], cell[1], cell[2]])

    def find_key_index(self, key: Any) -> tuple:
        hashed_key = hash(key)
        key_index = hashed_key % self.length
        while self.hash_table[key_index]:
            if (key == self.hash_table[key_index][0]
                    and hashed_key == self.hash_table[key_index][1]):
                return key_index, hashed_key, False
            key_index = (key_index + 1) % self.length

        return key_index, hashed_key, True

    def clear(self) -> None:
        self.length = self.initial_length
        self.hash_table = [[] for _ in range(self.length)]

    def __delitem__(self, key: Any) -> None:
        key_index, _, empty = self.find_key_index(key)
        if not empty:
            self.hash_table[key_index] = []
            return

        raise KeyError(f"Key {key} not found")

    def pop(self, key: Any) -> Any:
        key_index, _, empty = self.find_key_index(key)
        if not empty:
            popped_value = self.hash_table[key_index][2]
            self.hash_table[key_index] = []
            return popped_value

        raise KeyError(f"Key {key} not found")

    def update(self, other: "Dictionary") -> None:
        for cell in other.hash_table:
            if cell:
                key, _, value = cell
                self[key] = value

    def __iter__(self) -> Iterable:
        keys = []
        for cell in self.hash_table:
            if cell:
                keys.append(cell[0])

        return iter(keys)

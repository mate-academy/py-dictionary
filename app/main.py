from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index: int = self._hash(key) % self.capacity
        if not self.table[index]:
            self.table[index] = [(key, value)]
            self.size += 1
        else:
            pairs = self.table[index]
            for i, (k, v) in enumerate(pairs):
                if k == key:
                    pairs[i] = (key, value)
                    return
            pairs.append((key, value))
            self.size += 1
        if self.size >= self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index: int = self._hash(key) % self.capacity
        pairs = self.table[index]
        if pairs:
            for k, v in pairs:
                if k == key:
                    return v
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: Hashable) -> int:
        return hash(key)

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table = [None] * new_capacity
        for pairs in self.table:
            if pairs:
                for key, value in pairs:
                    index: int = self._hash(key) % new_capacity
                    if not new_table[index]:
                        new_table[index] = [(key, value)]
                    else:
                        new_table[index].append((key, value))
        self.table = new_table
        self.capacity = new_capacity

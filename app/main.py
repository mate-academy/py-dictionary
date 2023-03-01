from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.66) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self._length = 0
        self.table = [None] * capacity

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, key: Any) -> None:
        hash_value = hash(key) % self.capacity
        while self.table[hash_value] is not None:
            if self.table[hash_value][0] == key:
                return self.table[hash_value][2]
            hash_value = (hash_value + 1) % self.capacity
        raise KeyError(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key) % self.capacity
        while self.table[hash_value] is not None \
                and self.table[hash_value][0] != key:
            hash_value = (hash_value + 1) % self.capacity
        if self.table[hash_value] is None:
            self._length += 1
        self.table[hash_value] = (key, self._length, value)
        if self._length / self.capacity > self.load_factor:
            self._resize()

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity
        for node in self.table:
            if node is not None:
                hash_value = hash(node[0]) % self.capacity
                while new_table[hash_value] is not None:
                    hash_value = (hash_value + 1) % self.capacity
                new_table[hash_value] = node
        self.table = new_table

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key) % self.capacity
        while self.table[hash_value] is not None:
            if self.table[hash_value][0] == key:
                self.table[hash_value] = None
                self._length -= 1
                return
            hash_value = (hash_value + 1) % self.capacity
        else:
            raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> int | None:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.__init__()

    def __iter__(self) -> None:
        for node in self.table:
            if node is not None:
                yield node[0]

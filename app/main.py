from typing import Hashable


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self._size = 0
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._table = [[] for _ in range(self._capacity)]

    def __setitem__(self, key: Hashable, value: any) -> None:
        index = self._get_index(key)
        for node in self._table[index]:
            if node[0] == key and node[1] == hash(key):
                node[2] = value
                return
        self._table[index].append([key, hash(key), value])
        self._size += 1
        if self._size > self._capacity * self._load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        chain = self._table[index]
        for node in chain:
            if node[0] == key and hash(key):
                return node[2]
        raise KeyError(key)

    def _resize(self) -> None:
        new_capacity = self._capacity * 2
        new_table = [[] for _ in range(new_capacity)]
        for chain in self._table:
            for key, _, value in chain:
                index = hash(key) % new_capacity
                new_table[index].append([key, hash(key), value])
        self._table = new_table
        self._capacity = new_capacity

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self._size

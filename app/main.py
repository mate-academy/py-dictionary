from typing import Any


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.table = []
        for _ in range(initial_capacity):
            self.table.append([])
        self.size = 0

    def __setitem__(self, key: int, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity

        bucked = self.table[index]

        for node in bucked:
            if node[0] == key:
                node[2] = value
                return

        bucked.append([key, hash_key, value])
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]
        for bucked in self.table:
            for node in bucked:
                key, hash_key, value = node
                new_index = hash(key) % new_capacity
                new_table[new_index].append([key, hash_key, value])

        self.table = new_table
        self.capacity = new_capacity

    def __getitem__(self, key: int) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        bucked = self.table[index]

        for node in bucked:
            if node[0] == key:
                return node[2]
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size

from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.hash(key) % self.capacity
        if self.hash_table[index] is None:
            self.hash_table[index] = []
        for pair_k_v in self.hash_table[index]:
            if pair_k_v[0] == key:
                pair_k_v[1] = value
                return
        self.hash_table[index].append([key, value])
        self.size += 1
        if self.size >= self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.hash(key) % self.capacity

        if self.hash_table[index] is not None:
            for pair in self.hash_table[index]:
                if pair[0] == key:
                    return pair[1]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    @staticmethod
    def hash(key: Hashable) -> int:
        return hash(key)

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for space in self.hash_table:
            if space is not None:
                for pair in space:
                    index = self.hash(pair[0]) % new_capacity
                    if new_table[index] is None:
                        new_table[index] = []
                    new_table[index].append(pair)

        self.capacity = new_capacity
        self.hash_table = new_table

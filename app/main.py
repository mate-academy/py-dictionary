from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = [[]] * self.capacity

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        init_hash_table = self.hash_table
        self.hash_table = [[]] * self.capacity

        for hash_k_v in init_hash_table:
            if hash_k_v:
                i_hash, key, value = hash_k_v
                self.__setitem__(key, value)

    def __setitem__(
            self,
            key: (int, float, str, tuple, bool),
            value: Any
    ) -> None:
        if self.length > self.threshold:
            self.resize()

        init_hash = hash(key)
        index = init_hash % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = init_hash, key, value
                self.length += 1
                break

            if (
                    init_hash == self.hash_table[index][0]
                    and key == self.hash_table[index][1]
            ):
                self.hash_table[index] = init_hash, key, value
                break

            index = (index + 1) % self.capacity

    def __getitem__(
            self,
            key: (int, float, str, tuple, bool)
    ) -> Any:
        init_hash = hash(key)
        index = init_hash % self.capacity
        while self.hash_table[index]:
            if (
                    init_hash == self.hash_table[index][0]
                    and key == self.hash_table[index][1]
            ):
                return self.hash_table[index][2]

            index = (index + 1) % self.capacity

        raise KeyError()

    def __len__(self) -> int:
        return self.length

from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.hash_table: list[None] = [None] * self.capacity
        self.threshold = 2 / 3
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index][0] != key
        ):
            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 >= self.threshold * self.capacity:
                self.resize()
                return self.__setitem__(key, value)

            self.size += 1

        self.hash_table[index] = (key, value)

    def resize(self) -> None:
        old_hash_table = self.hash_table

        self.__init__(self.capacity * 2)
        [self.__setitem__(item[0], item[1]) for item in old_hash_table if item]

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if self.hash_table[index] is None:
            raise KeyError
        return self.hash_table[index][1]

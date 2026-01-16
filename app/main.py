from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self. capacity = 8
        self.storage = [None] * self.capacity
        self.length = 0

    def _resize(self) -> None:
        old_storage = self.storage
        self.capacity *= 2
        self.storage = [None] * self.capacity
        self.length = 0

        for bucket in old_storage:
            if bucket:
                for pair_k_v in bucket:
                    self.__setitem__(pair_k_v[0], pair_k_v[1])

    def _hash(self, key: Hashable) -> Any:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length + 1 > self.capacity * self.load_factor:
            self._resize()

        index = self._hash(key)
        while True:
            if self.storage[index] is None:
                self.storage[index] = [(key, value)]
                self.length += 1
                return

            for i, pair_k_v in enumerate(self.storage[index]):
                if pair_k_v[0] == key:
                    self.storage[index][i] = (key, value)
                    return
            self.storage[index].append((key, value))
            self.length += 1

    def __getitem__(self, key: Hashable) -> None:
        index = self._hash(key)

        if self.storage[index] is not None:
            for pair in self.storage[index]:
                if pair[0] == key:
                    return pair[1]
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

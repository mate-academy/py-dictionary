from typing import Any


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.66
    ) -> None:
        self.capacity = initial_capacity
        self.table = [[] for _ in range(self.capacity)]
        self.load_factor = load_factor
        self.count = 0

    def __setitem__(self, key: object, value: Any) -> None:
        hash_code = hash(key)
        index = hash_code % self.capacity
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
        self.count += 1
        if self.count >= self.capacity * self.load_factor:
            self._resize()

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self[key] = value

    def __getitem__(self, key: object) -> Any:
        hash_code = hash(key)
        index = hash_code % self.capacity
        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self) -> int:
        return self.count
